import pytest
import time
from playwright.sync_api import sync_playwright, expect

# Individual test execution MUST NOT exceed 10 seconds.
MAX_TEST_TIME = 10.0

@pytest.fixture(scope="function")
def mobile_page(server):
    with sync_playwright() as p:
        # Emulate Pixel 5
        device = p.devices['Pixel 5']
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(**device)
        page = context.new_page()
        page.goto(server, timeout=10000)
        page.wait_for_selector("#tab-bar", timeout=5000)
        yield page
        context.close()
        browser.close()

@pytest.mark.timeout(10)
def test_mobile_ghost_scroll(mobile_page):
    """Verify that Ghost Scroll overlay handles momentum and interactivity."""
    # Wait for either the terminal or any button in the active launcher tab
    mobile_page.wait_for_function("""
        () => document.querySelector('.xterm-screen') || 
              Array.from(document.querySelectorAll('.tab-instance.active button')).find(b => b.innerText.includes('Start New'))
    """, timeout=8000)

    if not mobile_page.locator('.xterm-screen').is_visible():
        mobile_page.locator('.tab-instance.active button').filter(has_text="Start New").first.click()
    
    mobile_page.wait_for_selector('.ghost-scroll', timeout=5000)
    
    ghost = mobile_page.locator('.ghost-scroll')
    
    # 1. Initial state: ghost should be pointer-events: none (transparent)
    expect(ghost).to_have_css("pointer-events", "none")
    
    # 2. Touchstart: ghost should become pointer-events: all (capture momentum)
    mobile_page.dispatch_event('.terminal-instance', 'touchstart')
    expect(ghost).to_have_css("pointer-events", "all")
    
    # 3. Touchend: ghost should eventually return to none
    mobile_page.dispatch_event('.terminal-instance', 'touchend')
    # Our logic uses a 1000ms timeout to allow momentum to play out
    time.sleep(1.2)
    expect(ghost).to_have_css("pointer-events", "none")
