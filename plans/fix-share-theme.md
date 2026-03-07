# Epic: Fix Shared Session CSS & Implement Theme Options

## Overview
Shared sessions look "wrecked" because the Xterm `serializeAddon` outputs raw HTML with inline CSS, but it lacks the correct outer container styles, CSS variables, and layout formatting needed to render exactly like the UI. We need to implement a full set of styles and give users a toggle (Dark/Light/Full Color) as previously planned, but also completely fix the base presentation of the `serializeAsHTML()` output.

## Details
1. **Fix `share.html` Layout & Spacing**:
   - The outer wrapper needs to be styled properly so the `pre` element fits and scrolls well without breaking.
   - Investigate injecting a customized wrapper or updating the `templates/share.html` to reset margins and box-sizing properly around the raw output.

2. **Implement Theme Options**:
   - As per previous tickets, users should be able to select Dark, Light, or Full Color.
   - Pass these options to `serializeAsHTML({ theme: 'dark', ... })` (if supported) OR apply CSS classes to the `<body>` of the shared page.

## Action Items
1. Check how the backend saves `htmlDump` into the database or template.
2. Ensure the CSS inside the shared page properly handles the `span` blocks that Xterm outputs.

## Tests
- E2E tests for exporting and validating the structural integrity of the shared HTML.