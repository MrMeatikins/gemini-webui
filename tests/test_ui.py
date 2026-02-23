import pytest
import time
from playwright.sync_api import sync_playwright, expect

# =====================================================================================
# MANDATORY TIMEOUT GUARDRAILS
# =====================================================================================
# This test has a history of hanging. Do NOT remove or increase these timeouts.
# Individual test execution MUST NOT exceed 20 seconds.
# =====================================================================================

MAX_TEST_TIME = 20.0

@pytest.mark.prone_to_timeout
@pytest.mark.timeout(20)
def test_gemini_ui_basic_interaction(server):
    import os
    print(f"DEBUG: Current directory: {os.getcwd()}")
    print(f"DEBUG: app.py path: {os.path.abspath('src/app.py')}")
    print(f"DEBUG: index.html path: {os.path.abspath('src/templates/index.html')}")
    start_time = time.time()
    
    def log_progress(step_name):
        elapsed = time.time() - start_time
        print(f"[TEST PROGRESS] {step_name} at {elapsed:.2f}s")
        if elapsed > MAX_TEST_TIME:
            pytest.fail(f"HARD TIMEOUT EXCEEDED: '{step_name}' took {elapsed:.2f}s which is > {MAX_TEST_TIME}s! Test execution is too slow.")
            
    log_progress("Starting test")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.on("console", lambda msg: print(f"CONSOLE [{time.time() - start_time:.2f}s]: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR [{time.time() - start_time:.2f}s]: {exc}"))
        
        try:
            # 1. Start the web interface
            log_progress("Navigating to server")
            page.goto(server, timeout=10000)
            page.wait_for_load_state("networkidle")
            
            # 2. Verify launcher is visible
            log_progress("Checking launcher presence")
            expect(page.get_by_text("Select a Connection")).to_be_visible(timeout=5000)
            
            # 3. Start a local session
            log_progress("Starting local session")
            start_btn = page.locator('button:has-text("Start New")').first
            start_btn.wait_for(state="visible", timeout=5000)
            start_btn.click()
            
            # 4. Verify connection status eventually shows 'local'
            log_progress("Checking connection status")
            status = page.locator('#connection-status')
            expect(status).to_have_text('local', timeout=10000)
            
            # 5. Open Settings
            log_progress("Opening settings")
            settings_btn = page.locator('button:has-text("Settings")')
            settings_btn.click(timeout=5000)
            expect(page.locator('#settings-modal')).to_be_visible(timeout=5000)
            
            # 6. Verify Manage Keys list is present
            log_progress("Checking Manage Keys list")
            key_list = page.locator('#key-list')
            key_list.wait_for(state="attached", timeout=10000)
            expect(key_list).to_be_attached(timeout=5000)
            
            # 7. Close settings
            log_progress("Closing settings")
            page.locator('#settings-modal span').first.click(timeout=5000)
            expect(page.locator('#settings-modal')).not_to_be_visible(timeout=5000)
            
            log_progress("Test steps completed successfully")
        except Exception as e:
            print("DEBUG: Page content on failure:")
            print(page.content())
            page.screenshot(path="failure_screenshot.png")
            raise e
        finally:
            log_progress("Cleaning up browser context")
            context.close()
            browser.close()
            
        elapsed_total = time.time() - start_time
        assert elapsed_total <= MAX_TEST_TIME, f"Test finished but exceeded MAX_TEST_TIME: {elapsed_total:.2f}s > {MAX_TEST_TIME}s."
