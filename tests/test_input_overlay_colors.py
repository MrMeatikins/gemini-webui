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

def test_input_overlay_colors(page):
    page.locator('.tab-instance.active button:has-text("Start New")').first.click()
    page.wait_for_selector(".xterm-helper-textarea", state="attached", timeout=10000)
    
    textarea = page.locator(".xterm-helper-textarea").first
    
    # "invoke the overlay box" using STT composition which makes it visually hold text
    long_text = "Testing overlay colors"
    textarea.evaluate("(el) => { el.dispatchEvent(new CompositionEvent('compositionstart')); }")
    textarea.evaluate(f"(el) => {{ el.value = `{long_text}`; el.dispatchEvent(new Event('input', {{ bubbles: true, inputType: 'insertCompositionText' }})); }}")
    
    # Check computed CSS
    colors = page.evaluate('''() => {
        const textarea = document.querySelector(".xterm-helper-textarea");
        const style = window.getComputedStyle(textarea);
        return {
            bg: style.backgroundColor,
            fg: style.color
        };
    }''')
    
    # We must definitively prevent a regression to black (rgb(0, 0, 0)) and white (rgb(255, 255, 255)).
    assert colors['bg'] != 'rgb(0, 0, 0)', "Regression detected: Overlay background is stark black."
    assert colors['fg'] != 'rgb(255, 255, 255)', "Regression detected: Overlay text is stark white."
    
    # Ensure it uses dark gray and light gray matching the terminal's theme
    # Default terminal theme: background #1e1e1e (30,30,30), foreground #d4d4d4 (212,212,212) or #cccccc (204,204,204)
    assert colors['bg'] == 'rgb(30, 30, 30)', f"Expected dark gray background, got {colors['bg']}"
    assert colors['fg'] in ['rgb(204, 204, 204)', 'rgb(212, 212, 212)'], f"Expected light gray foreground, got {colors['fg']}"