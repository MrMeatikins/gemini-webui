from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
            page = browser.contexts[0].pages[0]
            page.get_by_role("button", name="Start New").first.click()
            time.sleep(3)
            
            result = page.evaluate("""() => {
                const tab = tabs.find(t => t.state === 'terminal');
                return tab.term.buffer.active.getLines(0, 50).map(l => l.translateToString(true)).join('\\n');
            }""")
            print(result)
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run()
