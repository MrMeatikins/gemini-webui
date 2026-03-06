import pytest
import time
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope="function")
def page(server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
        page.goto(server, timeout=15000)
        page.wait_for_selector(".launcher, .terminal-instance", state="attached", timeout=15000)
        yield page
        context.close()
        browser.close()

def test_getLauncherWarningHtml_critical(page):
    """Test getLauncherWarningHtml returns critical warning when no storage is writable."""
    result = page.evaluate('''() => {
        const config = { DATA_WRITABLE: false, TMP_WRITABLE: false };
        return getLauncherWarningHtml(config);
    }''')
    assert "CRITICAL: No writable storage found." in result

def test_getLauncherWarningHtml_warning(page):
    """Test getLauncherWarningHtml returns warning when only data is not writable."""
    result = page.evaluate('''() => {
        const config = { DATA_WRITABLE: false, TMP_WRITABLE: true };
        return getLauncherWarningHtml(config);
    }''')
    assert "WARNING:</strong> Persistent storage (/data) is not writable." in result

def test_getLauncherWarningHtml_none(page):
    """Test getLauncherWarningHtml returns empty string when storage is writable."""
    result = page.evaluate('''() => {
        const config = { DATA_WRITABLE: true, TMP_WRITABLE: true };
        return getLauncherWarningHtml(config);
    }''')
    assert result == ""

def test_getLauncherHtml_contains_elements(page):
    """Test getLauncherHtml returns the basic HTML structure."""
    result = page.evaluate('''() => {
        return getLauncherHtml('test_id', '<div id="test_warning">Warning</div>');
    }''')
    assert '<div id="test_warning">Warning</div>' in result
    assert 'Select a Connection' in result
    assert 'id="test_id_quick_input"' in result
    assert 'id="test_id_connections"' in result
    assert 'id="test_id_backend_sessions"' in result

def test_renderLauncher_e2e(page):
    """Test that renderLauncher successfully creates the DOM elements."""
    # Ensure launcher is present
    expect(page.locator('.launcher').first).to_be_visible(timeout=5000)
    
    # Check that connection cards exist
    expect(page.locator('.connection-card').first).to_be_visible(timeout=5000)
    
    # Check that Quick Connect exists
    expect(page.locator('.quick-connect-bar').first).to_be_visible(timeout=5000)
