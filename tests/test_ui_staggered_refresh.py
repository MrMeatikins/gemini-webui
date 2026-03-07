import pytest
import time
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope="function")
def staggered_page(server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Mock /api/hosts to return 3 hosts
        page.route("**/api/hosts", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='[{"label": "host1", "type": "local"}, {"label": "host2", "type": "local"}, {"label": "host3", "type": "local"}]'
        ))

        # Track session requests
        page.session_requests = []
        def track_request(request):
            if "/api/sessions" in request.url and "cache=true" in request.url:
                page.session_requests.append(time.time())
        page.on("request", track_request)

        page.route("**/api/health/*", lambda route: route.fulfill(status=200, body='{"status":"up"}'))
        
        page.goto(server, timeout=15000)
        page.wait_for_selector(".launcher, .terminal-instance", state="attached", timeout=15000)
        yield page
        context.close()
        browser.close()

def test_staggered_initial_load(staggered_page):
    # Wait for the stagger to complete (3 requests * 500ms = ~1500ms)
    staggered_page.wait_for_timeout(3000)
    
    assert len(staggered_page.session_requests) >= 3, f"Expected at least 3 session requests, got {len(staggered_page.session_requests)}"
    
    # Calculate intervals between the first 3 requests
    intervals = []
    for i in range(1, 3):
        intervals.append(staggered_page.session_requests[i] - staggered_page.session_requests[i-1])
        
    print(f"Session requests times: {staggered_page.session_requests}")
    print(f"Stagger intervals: {intervals}")
    
    # We expect intervals to be ~0.5s, check that they are at least somewhat staggered (e.g. > 0.3s)
    assert intervals[0] > 0.25, f"First stagger too short: {intervals[0]}s"
    assert intervals[1] > 0.25, f"Second stagger too short: {intervals[1]}s"
