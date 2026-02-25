from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://172.22.0.10:9222")
            page = browser.contexts[0].pages[0]
            
            result = page.evaluate("""() => {
                return {
                    typeof: typeof window.WebLinksAddon,
                    toString: window.WebLinksAddon ? window.WebLinksAddon.toString() : 'null',
                    hasWebLinksAddonProp: window.WebLinksAddon && !!window.WebLinksAddon.WebLinksAddon
                };
            }""")
            print(result)
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run()
