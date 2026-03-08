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

def test_stt_color(page):
    page.locator('.tab-instance.active button:has-text("Start New")').first.click()
    page.wait_for_selector(".xterm-helper-textarea", state="attached", timeout=10000)
    textarea = page.locator(".xterm-helper-textarea").first
    
    # Simulate Voice Typing (STT)
    long_text = "Testing STT"
    textarea.evaluate("(el) => { el.dispatchEvent(new CompositionEvent('compositionstart')); }")
    textarea.evaluate(f"(el) => {{ el.value = `{long_text}`; el.dispatchEvent(new Event('input', {{ bubbles: true, inputType: 'insertCompositionText' }})); }}")
    
    # Check computed style during composition
    style = page.evaluate('''() => {
        const el = document.querySelector(".xterm-helper-textarea");
        const style = window.getComputedStyle(el);
        return { bg: style.backgroundColor, fg: style.color };
    }''')
    print("Computed Styles during STT:", style)

    assert style['bg'] == 'rgb(30, 30, 30)', f"Expected 'rgb(30, 30, 30)', got {style['bg']}"
    assert style['fg'] == 'rgb(212, 212, 212)', f"Expected 'rgb(212, 212, 212)', got {style['fg']}"
