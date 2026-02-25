from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
        contexts = browser.contexts
        if not contexts:
            print("No browser contexts found.")
            return
        
        # Look for a context with pages
        page = None
        for context in contexts:
            if context.pages:
                page = context.pages[0]
                break
                
        if not page:
            print("No pages found in the browser.")
            return
            
        print(f"Connected to page: {page.url}")
        page.screenshot(path="openclaw_browser.png")
        print("Screenshot saved to openclaw_browser.png")
        browser.close()

if __name__ == "__main__":
    run()
