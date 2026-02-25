from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
            page = browser.contexts[0].pages[0]
            
            logs = []
            page.on("console", lambda msg: logs.append(msg.text))
            
            print("Reloading page...")
            page.reload()
            time.sleep(2)
            
            print("Starting session...")
            page.get_by_role("button", name="Start New").first.click()
            time.sleep(2)
            
            print("Hovering to trigger link detection...")
            # We need to hover over the actual terminal rows
            # Based on the screenshot, the link is near the top
            for y in range(150, 250, 10):
                page.mouse.move(200, y)
                time.sleep(0.1)
            
            print("--- Browser Console Logs ---")
            for log in logs:
                print(log)
            print("--- End Logs ---")
            
            result = page.evaluate("""() => {
                const links = document.querySelectorAll('.xterm-link');
                return {
                    count: links.length
                };
            }""")
            print(f"Link detection result: {result}")
            
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run()
