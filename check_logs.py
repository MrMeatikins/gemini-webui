from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
            page = browser.contexts[0].pages[0]
            
            # Get console logs
            logs = []
            page.on("console", lambda msg: logs.append(msg.text))
            
            # Refresh page to trigger initialization if needed, but let's just wait first
            time.sleep(2)
            
            print("--- Browser Console Logs ---")
            for log in logs:
                print(log)
            print("--- End Logs ---")
            
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run()
