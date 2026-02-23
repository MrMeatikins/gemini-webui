import pytest
import time
from playwright.sync_api import sync_playwright, expect

# =====================================================================================
# MANDATORY TIMEOUT GUARDRAILS
# =====================================================================================
# Individual test execution MUST NOT exceed 20 seconds.
# =====================================================================================

MAX_TEST_TIME = 20.0

@pytest.mark.prone_to_timeout
@pytest.mark.timeout(20)
def test_gemini_ui_comprehensive(server):
    start_time = time.time()
    
    def log_progress(step_name):
        elapsed = time.time() - start_time
        print(f"[TEST PROGRESS] {step_name} at {elapsed:.2f}s")
        if elapsed > MAX_TEST_TIME:
            pytest.fail(f"HARD TIMEOUT EXCEEDED: '{step_name}' took {elapsed:.2f}s!")
            
    log_progress("Starting comprehensive test")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 1. Start and handle potential auto-resume
            log_progress("Navigating to server")
            page.goto(server, timeout=10000)
            page.wait_for_load_state("networkidle")
            
            # If auto-resume kicked in, we might be in terminal. 
            # We want to test launcher, so we open a new tab which always starts at launcher.
            log_progress("Ensuring we see the launcher")
            launcher_header = page.get_by_text("Select a Connection")
            if not launcher_header.is_visible():
                log_progress("Auto-resume detected, opening a new tab to see launcher")
                page.locator('#new-tab-btn').click()
                expect(page.get_by_text("Select a Connection")).to_be_visible(timeout=5000)
            
            # 2. Test tab closing
            log_progress("Testing tab closing")
            initial_tabs = page.locator('.tab').count()
            page.locator('#new-tab-btn').click()
            expect(page.locator('.tab')).to_have_count(initial_tabs + 1)
            page.locator('.tab-close').last.click()
            expect(page.locator('.tab')).to_have_count(initial_tabs)
            
            # 3. Start session and verify terminal
            log_progress("Starting local session")
            page.locator('button.primary:has-text("Start New")').first.click()
            
            # 4. Verify cursor and focus
            log_progress("Verifying terminal focus and cursor")
            expect(page.locator('.xterm-helper-textarea').last).to_be_focused(timeout=5000)
            
            # 5. Verify 256 color support and theme
            log_progress("Verifying 256-color theme")
            bg_color = page.evaluate("window.getComputedStyle(document.querySelector('.xterm-viewport')).backgroundColor")
            assert bg_color == "rgb(30, 30, 30)" # #1e1e1e
            
            # 6. Verify Manage Hosts in settings
            log_progress("Opening settings to check hosts")
            settings_btn = page.locator('button:has-text("Settings")')
            settings_btn.click()
            expect(page.locator('#hosts-list')).to_be_visible(timeout=5000)
            
            log_progress("Test completed successfully")
        except Exception as e:
            page.screenshot(path="failure_screenshot.png")
            raise e
        finally:
            context.close()
            browser.close()
