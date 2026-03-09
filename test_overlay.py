import pytest
from playwright.sync_api import sync_playwright

def test_overlay_color():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:5000")
        
        # Start a session
        page.locator('.tab-instance.active button:has-text("Start New")').first.click()
        page.wait_for_selector(".xterm-helper-textarea")
        
        # Evaluate styles
        style = page.evaluate('''() => {
            const el = document.querySelector(".xterm-helper-textarea");
            const style = window.getComputedStyle(el);
            return { bg: style.backgroundColor, fg: style.color };
        }''')
        
        print("Computed Styles:", style)
        browser.close()

if __name__ == "__main__":
    test_overlay_color()
