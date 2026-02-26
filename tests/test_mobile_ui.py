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
def test_mobile_touch_passthrough(mobile_page):
    """Verify that pointer-events toggle on xterm-screen during touch."""
    # Start a session
    mobile_page.locator('.tab-instance.active button:has-text("Start New")').first.click()
    mobile_page.wait_for_selector('.xterm-screen', timeout=5000)
    
    screen = mobile_page.locator('.xterm-screen')
    
    # 1. Initially pointer-events should be 'auto' or 'all' (default/applied)
    # The CSS sets it to 'none' via @media query, so we check that
    expect(screen).to_have_css("pointer-events", "none")
    
    # 2. Trigger touchstart
    mobile_page.dispatch_event('.terminal-instance', 'touchstart')
    expect(screen).to_have_css("pointer-events", "none")
    
    # 3. Trigger touchend
    mobile_page.dispatch_event('.terminal-instance', 'touchend')
    # After touchend, it should be re-enabled to 'all' by our JS
    expect(screen).to_have_css("pointer-events", "all")
