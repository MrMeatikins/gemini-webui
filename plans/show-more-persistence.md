# Fix "Show More" session persistence

## Details of what's required
When expanding the session list on the connection page (e.g., clicking "show 98 more"), it currently takes around 5 seconds to load the full list, and then it clears and collapses back to the default view the next time a background ping or auto-refresh occurs. 

1. **Investigate Data Fetching**: Determine why it takes ~5 seconds to expand the list. If it is fetching data synchronously or executing an expensive query, optimize it.
2. **State Persistence**: The expanded state (`forceAll = true` or equivalent) must be maintained across polling intervals or pings. If a user clicks "show X more", the UI should stay expanded until explicitly collapsed or until the user navigates away.
3. **Logic Update**: Modify the session fetching or rendering logic (likely in `src/static/app.js` and/or `src/app.py` / `src/process_manager.py`) so that background updates preserve the user's expanded view.

## Test recommendations
- Click "show X more" and ensure it expands quickly.
- Wait for a background ping/refresh (or trigger one manually) and verify that the session list remains fully expanded.
- Verify that closing the expanded view or navigating to a different connection works as expected.

## Definition of Done
- The session list no longer collapses unexpectedly on background refresh.
- Performance of expanding the list is analyzed and improved if it was due to redundant requests.
- All relevant UI states are persistent during active viewing.