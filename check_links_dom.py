from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
            page = browser.contexts[0].pages[0]
            
            # The URL starts at line 3 roughly
            # Xterm rows are divs or canvas. In 5.x it's often a canvas but the linkifier adds overlays.
            
            print("Hovering over line 3...")
            # Try to hit the URL
            page.mouse.move(200, 180) 
            time.sleep(1)
            
            # Check if an anchor or span with xterm-link appeared
            result = page.evaluate("""() => {
                const links = document.querySelectorAll('.xterm-link');
                return {
                    count: links.length,
                    innerHTML: Array.from(links).map(l => l.innerHTML)
                };
            }""")
            print(f"DOM Links: {result}")
            
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run()
