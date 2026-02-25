from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
            # We don't want to create a new page, just see what's there
            pages = []
            for context in browser.contexts:
                pages.extend(context.pages)
            
            if not pages:
                print("No open pages found.")
                return

            # Take a screenshot of each page to be sure
            for i, page in enumerate(pages):
                print(f"Page {i}: {page.url}")
                page.screenshot(path=f"peek_page_{i}.png")
            
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run()
