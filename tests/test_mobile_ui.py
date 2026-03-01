import pytest
import time
from playwright.sync_api import sync_playwright, expect

# Individual test execution MUST NOT exceed 20 seconds.
MAX_TEST_TIME = 20.0

@pytest.fixture(scope="function")
def mobile_page(server):
    with sync_playwright() as p:
        # Emulate Pixel 5
        device = p.devices['Pixel 5']
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(**device)
        page = context.new_page()
        page.goto(server, timeout=15000)
        page.wait_for_selector(".launcher, .terminal-instance", state="attached", timeout=15000)
        yield page
        context.close()
        browser.close()

@pytest.mark.timeout(20)
def test_mobile_ui_exists(mobile_page):
    """Verify that mobile UI is functional."""
    mobile_page.wait_for_selector("#tab-bar", timeout=5000)

@pytest.mark.timeout(20)
def test_mobile_controls_buttons(mobile_page):
    """Verify that all mobile control buttons exist."""
    # 1. Start a local session
    # The first "Start New" button is for the 'local' connection
    mobile_page.click("text=Start New")
    mobile_page.wait_for_selector(".terminal-instance", timeout=10000)
    
    # 2. Check mobile controls visibility
    # Wait for the mobile controls to be visible
    mobile_page.wait_for_selector("#mobile-controls", state="visible", timeout=5000)
    
    # Debug: Print the innerHTML of the controls
    html = mobile_page.locator("#mobile-controls").inner_html()
    print("DEBUG HTML:", html)
    
    # 3. Check for specific buttons
    expected_buttons = ["Esc", "Tab", "Ctrl", "Alt", "▲", "▼", "◀", "▶", "A+", "A-", "Home", "End"]
    for btn_text in expected_buttons:
        btn = mobile_page.locator("#mobile-controls .control-btn").get_by_text(btn_text, exact=True)
        expect(btn.first).to_be_visible()
