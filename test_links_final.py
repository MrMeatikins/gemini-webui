from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
            page = browser.contexts[0].pages[0]
            
            page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
            
            print("Reloading...")
            page.reload()
            time.sleep(2)
            
            print("Starting session...")
            page.get_by_role("button", name="Start New").first.click()
            time.sleep(2)
            
            # Hover over the terminal to trigger providers
            # The URL is usually around the top
            print("Hovering over terminal...")
            for y in range(100, 300, 10):
                page.mouse.move(200, y)
                time.sleep(0.05)
            
            # Check for detected links in terminal buffer via evaluate
            result = page.evaluate("""() => {
                const tab = tabs.find(t => t.state === 'terminal');
                if (!tab) return "No terminal tab";
                
                // Let's force detection on a few lines
                const results = [];
                for (let i = 1; i <= 10; i++) {
                    tab.term.registerLinkProvider({
                        provideLinks(y, cb) {
                            if (y === i) {
                                // This is just to test if the terminal is calling us
                                console.log("TERMINAL CALLED provideLinks for line " + y);
                            }
                            cb(undefined);
                        }
                    });
                }
                return "Registered debug providers";
            }""")
            
            # Move mouse again to trigger the new providers
            for y in range(100, 300, 10):
                page.mouse.move(200, y)
                time.sleep(0.05)
                
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run()
