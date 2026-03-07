const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
  
  await page.goto('http://127.0.0.1:7787');
  
  // start session
  await page.click('div[data-label="local"] button:has-text("Start New")');
  await page.waitForSelector('.terminal-instance');
  
  // click new tab
  await page.click('#new-tab-btn');
  await page.waitForSelector('.launcher');
  
  // Wait for the backend session item
  await page.waitForSelector('.session-item');
  
  // Set marker
  await page.evaluate(() => {
     const item = document.querySelector('.session-item');
     item.setAttribute('data-test-marker', 'persisted');
     console.log('Set marker on item id:', item.id);
  });
  
  // Refresh
  await page.evaluate(() => {
     const activeTab = document.querySelector('.tab-content.active');
     const id = activeTab.id.replace('_instance', '');
     console.log('Refreshing with id:', id);
     
     // Let's hook fetch
     const originalFetch = window.fetch;
     window.fetch = async (...args) => {
         console.log('Fetch called for', args[0]);
         return originalFetch(...args);
     };
     
     refreshBackendSessionsList(id);
  });
  
  await page.waitForTimeout(2000);
  
  const marker = await page.evaluate(() => {
     const item = document.querySelector('.session-item');
     console.log('Item after refresh id:', item ? item.id : 'none');
     return item ? item.getAttribute('data-test-marker') : null;
  });
  
  console.log('MARKER IS:', marker);
  await browser.close();
})();
