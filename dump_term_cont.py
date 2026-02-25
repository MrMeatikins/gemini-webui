from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
            page = browser.contexts[0].pages[0]
            
            print("Dumping lines 20-50...")
            result = page.evaluate("""() => {
                const tab = tabs.find(t => t.state === 'terminal');
                if (!tab) return ["No terminal"];
                const term = tab.term;
                const lines = [];
                for (let i = 20; i < Math.min(50, term.buffer.active.length); i++) {
                    const line = term.buffer.active.getLine(i);
                    if (line) lines.push(line.translateToString(true));
                }
                return lines;
            }""")
            for i, line in enumerate(result):
                print(f"{i+20}: {line}")
                
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run()
