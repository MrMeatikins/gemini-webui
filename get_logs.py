from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
    
    print("Navigating to http://localhost:5000")
    try:
        page.goto("http://localhost:5000", timeout=5000)
        page.wait_for_timeout(2000)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        browser.close()
