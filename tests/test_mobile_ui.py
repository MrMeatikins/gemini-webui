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
def test_mobile_momentum_config(mobile_page):
    """Verify that CSS momentum scrolling rules are applied on mobile."""
    # Wait for either the terminal or any button in the active launcher tab
    mobile_page.wait_for_function("""
        () => document.querySelector('.xterm-screen') || 
              Array.from(document.querySelectorAll('.tab-instance.active button')).find(b => b.innerText.includes('Start New'))
    """, timeout=8000)

    if not mobile_page.locator('.xterm-screen').is_visible():
        mobile_page.locator('.tab-instance.active button').filter(has_text="Start New").first.click()
    
    mobile_page.wait_for_selector('.xterm-screen', timeout=5000)
    
    screen = mobile_page.locator('.xterm-screen')
    viewport = mobile_page.locator('.xterm-viewport')
    
    # 1. Screen should have pointer-events: none to allow swipe passthrough
    expect(screen).to_have_css("pointer-events", "none")
    
    # 2. Viewport should have pointer-events: all and be roughly full width
    expect(viewport).to_have_css("pointer-events", "all")
    
    # Verify it's at least as wide as the terminal content (allowing for padding)
    is_full_width = viewport.evaluate("""el => {
        const parentWidth = el.parentElement.clientWidth;
        return Math.abs(el.clientWidth - parentWidth) <= 2;
    }""")
    assert is_full_width, f"Viewport width {viewport.evaluate('el => el.clientWidth')} should match parent width"
    
    # 3. Interactive bits should still have pointer-events: all
    helpers = mobile_page.locator('.xterm-helpers')
    expect(helpers).to_have_css("pointer-events", "all")
