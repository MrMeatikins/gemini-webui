import re

with open('src/static/app.js', 'r') as f:
    content = f.read()

# Fix Backend Managed Sessions pulse logic
content = re.sub(
    r'if \(backendSessionLastSeen\[s\.tab_id\] && backendSessionLastSeen\[s\.tab_id\] !== s\.last_active\) {\s*shouldPulse = true;\s*}',
    '',
    content
)

# Fix HostStateManager updateHealth to absolutely prevent pulse on polling unless state changes
content = re.sub(
    r'updateHealth: function\(tabId, label, isSuccess, shouldPulse = true\) \{',
    'updateHealth: function(tabId, label, isSuccess, shouldPulse = false) {',
    content
)

# And in fetchSessions where it's called on success:
# Let's ensure it ONLY pulses on state change.
with open('src/static/app.js', 'w') as f:
    f.write(content)
