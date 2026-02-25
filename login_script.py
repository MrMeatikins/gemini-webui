from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
        contexts = browser.contexts
        context = contexts[0] if contexts else browser.new_context()
        page = context.pages[0] if context.pages else context.new_page()
        
        # Listen to console
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Browser error: {err}"))
        page.on("response", lambda response: print(f"Response: {response.url} - {response.status}"))
        
        print("Navigating to https://gemini.hackedyour.info/")
        page.goto("https://admin:admin@gemini.hackedyour.info/")
        
        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    run()
