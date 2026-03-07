import pytest
from playwright.sync_api import sync_playwright, expect
import time

def test_theory(server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        def handle_route(route):
            route.fulfill(status=500, body="Internal Server Error")
        page.route("**/api/sessions*", handle_route)
        
        page.goto(server, timeout=15000)
        page.wait_for_selector(".launcher", state="attached", timeout=15000)
        
        local_health = page.locator('div[data-label="local"] .connection-title span[id$="_health_local"]')
        
        # Initially white because the cache request fails and skips
        expect(local_health).to_have_text("⚪", timeout=5000)
        
        page.evaluate('''() => {
            if (typeof activeTabId !== "undefined") {
                const id = activeTabId;
                const sessionListId = `${id}_sessions_local`;
                fetchSessions(id, {label: 'local', type: 'local'}, sessionListId, false, false);
            }
        }''')
        
        # It should become red after the manual fetch fails
        expect(local_health).to_have_text("🔴", timeout=5000)
        context.close()
        browser.close()
