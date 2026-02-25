from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
            page = browser.contexts[0].pages[0]
            
            logs = []
            page.on("console", lambda msg: logs.append(msg.text))
            
            print("Reloading...")
            page.reload()
            time.sleep(2)
            
            print("Starting session...")
            page.get_by_role("button", name="Start New").first.click()
            time.sleep(3)
            
            print("Hovering to trigger links...")
            for y in range(150, 300, 10):
                page.mouse.move(300, y)
                time.sleep(0.05)
            
            print("--- Browser Logs ---")
            for log in logs:
                if "LINE" in log or "MATCHED" in log or "gemini" in log:
                    print(log)
            print("--- End Logs ---")
            
            result = page.evaluate("""() => {
                const tab = tabs.find(t => t.state === 'terminal');
                const lines = [];
                for (let i = 0; i < 20; i++) {
                    const l = tab.term.buffer.active.getLine(i);
                    if (l) lines.push(l.translateToString(true));
                }
                return lines.join('\\n');
            }""")
            print("--- Terminal Content ---")
            print(result)
            
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run()
