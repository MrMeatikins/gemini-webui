import re

with open('src/static/app.js', 'r') as f:
    js = f.read()

# 1. Fix Connection Cards to only pulse on actual state change (or if explicitly requested, but polling is false)
js = re.sub(
    r'updateHealth: function\(tabId, label, isSuccess, shouldPulse = true\) \{',
    'updateHealth: function(tabId, label, isSuccess, shouldPulse = false) {',
    js
)

# 2. Fix Backend Managed Sessions to pulse on ANY state confirmation (active->active, etc)
# To do this, we ensure it ALWAYS pulses when it is successfully refreshed!
replacement = """
                    let shouldPulse = true; // Always pulse on update for animated indicators (active->active, etc)
                    const pulseId = `${id}_backend_pulse_${s.tab_id}`;
                    let pulseHtml = `<div id="${pulseId}" class="pulse-indicator"></div>`;

                    backendSessionLastSeen[s.tab_id] = s.last_active;
                    backendSessionStatusClass[s.tab_id] = statusClass;
"""

js = re.sub(
    r'let shouldPulse = false;.*?backendSessionStatusClass\[s\.tab_id\] = statusClass;',
    replacement.strip(),
    js,
    flags=re.DOTALL
)

with open('src/static/app.js', 'w') as f:
    f.write(js)

