import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page(server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(server, timeout=15000)
        yield page
        context.close()
        browser.close()

def test_overlay_box_colors_match_terminal_theme(page):
    page.locator('.tab-instance.active button:has-text("Start New")').first.click()
    page.wait_for_selector(".xterm-helper-textarea", state="attached", timeout=10000)
    
    textarea = page.locator(".xterm-helper-textarea").first
    
    # Simulate Voice Typing (STT) to invoke overlay
    long_text = "Testing STT"
    textarea.evaluate("(el) => { el.dispatchEvent(new CompositionEvent('compositionstart')); }")
    textarea.evaluate(f"(el) => {{ el.value = `{long_text}`; el.dispatchEvent(new Event('input', {{ bubbles: true, inputType: 'insertCompositionText' }})); }}")
    
    # Get computed styles
    colors = page.evaluate('''() => {
        const textarea = document.querySelector(".xterm-helper-textarea");
        const style = window.getComputedStyle(textarea);
        return {
            bg: style.backgroundColor,
            fg: style.color
        };
    }''')
    
    # We expect them to match the terminal theme which is #1e1e1e and #cccccc in hex.
    # In Playwright evaluate, getComputedStyle returns rgb() values.
    # #1e1e1e is rgb(30, 30, 30).
    # #cccccc is rgb(204, 204, 204)
    # The default JS might use different defaults if not careful, but our goal is 
    # to avoid stark black (#000000) and white (#ffffff) or #444/white.
    
    # Check that it's definitively not black and white
    assert colors['bg'] != 'rgb(0, 0, 0)', "Regression: Background is stark black!"
    assert colors['fg'] != 'rgb(255, 255, 255)', "Regression: Foreground is stark white!"
    
    # Check that it matches the transparent background and light gray foreground
    # Allowing for rgba(0, 0, 0, 0) and #cccccc (204,204,204) or #d4d4d4 (212,212,212)
    assert colors['bg'] in ['rgba(0, 0, 0, 0)', 'transparent'], f"Expected transparent background, got {colors['bg']}"
    assert colors['fg'] in ['rgb(204, 204, 204)', 'rgb(212, 212, 212)', 'rgb(229, 229, 229)'], f"Expected light gray foreground, got {colors['fg']}"

