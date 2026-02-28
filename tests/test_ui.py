import pytest
import time
from playwright.sync_api import sync_playwright, expect

# =====================================================================================
# MANDATORY TIMEOUT GUARDRAILS
# =====================================================================================
# Individual test execution MUST NOT exceed 20 seconds.
# =====================================================================================

MAX_TEST_TIME = 20.0

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

@pytest.mark.prone_to_timeout
@pytest.mark.timeout(20)
def test_ui_launcher_and_sessions(page):
    """Verify launcher opens and displays mock sessions."""
    # Launcher is open by default on first load
    expect(page.get_by_text("Select a Connection").first).to_be_visible(timeout=5000)
    # Check for pre-loaded mock sessions
    expect(page.get_by_text("Mock Session").first).to_be_visible(timeout=5000)

@pytest.mark.prone_to_timeout
@pytest.mark.timeout(20)
def test_ui_local_protection(page):
    """Verify the default 'local' host is protected from deletion."""
    page.locator('button:has-text("Settings")').click()
    expect(page.locator('#hosts-list')).to_contain_text("local")
    
    import re
    local_host_item = page.locator("#hosts-list .session-item").filter(
        has=page.locator("span", has_text=re.compile(r"^local$"))
    ).first
    # Delete button should NOT exist for local
    expect(local_host_item.locator("button:has-text('Delete')")).to_have_count(0)

@pytest.mark.prone_to_timeout
@pytest.mark.timeout(20)
def test_ui_terminal_initialization(page):
    """Verify terminal starts and sensitive inputs are removed."""
    # Open a new tab to ensure we are in launcher mode
    page.locator('#new-tab-btn').click()
    
    # Click "Start New" on local (first card) in the ACTIVE tab
    btns = page.locator('.tab-instance.active button:has-text("Start New")')
    expect(btns.first).to_be_visible(timeout=5000)
    btns.first.click()
    
    # Wait for terminal to appear
    expect(page.locator('#active-connection-info')).to_be_visible(timeout=5000)
    # Verify Restart button is there
    expect(page.locator('button:has-text("Restart")')).to_be_visible()
    # SECURITY: Verify ssh-target and ssh-dir are NOT in the DOM
    expect(page.locator('#ssh-target')).to_have_count(0)
    expect(page.locator('#ssh-dir')).to_have_count(0)

@pytest.mark.prone_to_timeout
@pytest.mark.timeout(20)
def test_ui_tab_management(page):
    """Verify creating and closing tabs works correctly."""
    # First, turn the initial tab into a terminal so we can create a second launcher tab
    btns = page.locator('.tab-instance.active button:has-text("Start New")')
    expect(btns.first).to_be_visible(timeout=5000)
    btns.first.click()
    expect(page.locator('#active-connection-info')).to_be_visible(timeout=5000)

    initial_tabs = page.locator('.tab').count()
    
    # Create new tab (this will now be allowed as it's the second launcher)
    page.locator('#new-tab-btn').click()
    expect(page.locator('.tab')).to_have_count(initial_tabs + 1)
    
    # Close tab
    page.locator('.tab-close').last.click()
    expect(page.locator('.tab')).to_have_count(initial_tabs)
