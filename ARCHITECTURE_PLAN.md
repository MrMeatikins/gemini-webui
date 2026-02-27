# Gemini WebUI Architecture: Session Reclaim & Multi-Device Sync

## Background & Rationale
The Gemini WebUI was originally designed around ephemeral browser connections handling raw PTY inputs and outputs. When a page refreshed, the frontend state (active tabs) was destroyed, leaving the backend PTY processes orphaned. While these orphaned processes were preserved for 60 seconds, there was no mechanism to recover them from a fresh UI state.

We have evaluated two major approaches to solving multi-monitor synchronization and cross-device persistence:
- **Approach A (Mirrored Backend):** Backend dictates UI state to all clients simultaneously. Discarded due to complex resizing conflicts (layout thrashing between mobile and desktop) and the inability to natively stream terminal states properly without a heavy multiplexer like `tmux`.
- **Approach B (Independent Windows):** Frontend (`sessionStorage`) dictates UI state. Backend acts as a dumb PTY host. Chosen for its clean separation of concerns, native multi-monitor support (different monitors can have different tabs open), and simplicity.

## The New System (Enhanced Approach B)
We are implementing **Approach B with an "Active Sessions" API** to re-introduce cross-device persistence. 

### Core Mechanics
1. **Frontend State (`sessionStorage`)**
   - The browser tab maintains its own UI state using `sessionStorage`. Opening a new window starts a fresh workspace.
   - PTY connections are mapped to stable UUIDs generated on the frontend.

2. **Backend Session Registry**
   - `app.py` is refactored to treat `persistent_ptys` as a robust registry containing metadata:
     - `tab_id` (UUID)
     - `title`
     - `ssh_target`, `ssh_dir`, `resume_state`
     - `last_active` timestamp
   - The backend enforces a resource limit (e.g., maximum 20 PTYs per user) to prevent descriptor exhaustion.

3. **Cross-Device Recovery ("Session Steal")**
   - When a new device (or a fresh browser window) connects, it can query `GET /api/sessions`.
   - It is presented with a list of currently active or orphaned sessions running on the server.
   - The user can select a session to "Reclaim" it.
   - **Session Stealing:** If Device B reclaims a session actively owned by Device A, the backend explicitly disconnects Device A's WebSocket for that specific PTY to prevent input/resizing conflicts. Device B assumes total control.

4. **Terminal State Integrity (`dtach` / `tmux`)**
   - *Current limitation:* Replaying a raw character buffer upon reconnection corrupts TUI applications (`vim`, `htop`).
   - *Next Step implementation:* The underlying `pty.fork` execution will be wrapped in `dtach` or `tmux` (or `abduco`) to natively decouple the process from the viewport and handle ANSI escape codes / screen redraws perfectly when a new device attaches.

## Development Environment
To maintain the integrity of the live instance during development:
- The development application is being run locally on a new port (`5001`).
- The backend leverages the `BYPASS_AUTH_FOR_TESTING=true` environment variable.
- The `chrome-devtools-mcp` extension has been configured to connect to the remote browser at `192.168.1.133:9222`.

## Next Action Items
1. Refactor `persistent_ptys` in `app.py` into a robust `SessionManager` class to store metadata.
2. Expose the `GET /api/sessions` endpoint.
3. Update `index.html` frontend to store tab data in `sessionStorage`.
4. Implement the "Reclaim Session" UI modal on the frontend.
5. Wrap the PTY execution in a multiplexer (`dtach` or `tmux`) to solve visual corruption on reclaim.