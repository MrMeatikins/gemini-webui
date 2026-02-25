from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
            page = browser.contexts[0].pages[0]
            
            # Start session to get content if needed
            # but maybe it's already there
            
            print("Dumping first 20 lines...")
            result = page.evaluate("""() => {
                const tab = tabs.find(t => t.state === 'terminal');
                if (!tab) return ["No terminal"];
                const term = tab.term;
                const lines = [];
                for (let i = 0; i < Math.min(20, term.buffer.active.length); i++) {
                    const line = term.buffer.active.getLine(i);
                    if (line) lines.push(line.translateToString(true));
                }
                return lines;
            }""")
            for i, line in enumerate(result):
                print(f"{i}: {line}")
                
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run()
