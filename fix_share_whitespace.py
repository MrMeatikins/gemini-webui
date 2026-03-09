import re

with open('src/static/app.js', 'r') as f:
    js = f.read()

replacement = """
            let htmlDump = serializeAddon.serializeAsHTML({
                includeGlobalBackground: selectedTheme === 'full'
            });

            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = htmlDump;

            // Xterm serialization usually wraps in a single root element
            const rootEl = tempDiv.firstElementChild || tempDiv;
            const lines = Array.from(rootEl.children);
            
            // Trim trailing empty lines to prevent massive whitespace
            while (lines.length > 0) {
                const lastLine = lines[lines.length - 1];
                if (!lastLine.textContent || !lastLine.textContent.replace(/\\u00a0/g, ' ').trim()) {
                    lastLine.remove();
                    lines.pop();
                } else {
                    break;
                }
            }

            if (selectedTheme === 'light' || selectedTheme === 'dark') {
                // Remove explicit color styles so CSS themes can apply
                for (const child of tempDiv.children) {
                    if (child.style) {
                        child.style.backgroundColor = '';
                        child.style.color = '';
                    }
                }
            }
            htmlDump = tempDiv.innerHTML;
"""

# Find the start and end of the block
start_str = "let htmlDump = serializeAddon.serializeAsHTML({"
end_str = "htmlDump = tempDiv.innerHTML;\n            }"

start_idx = js.find(start_str)
end_idx = js.find(end_str) + len(end_str)

if start_idx != -1 and end_idx != -1:
    js = js[:start_idx] + replacement.strip() + js[end_idx:]

# Disable the dropdown after generation:
js = js.replace("document.getElementById('confirm-share-btn').style.display = 'none';", 
                "document.getElementById('confirm-share-btn').style.display = 'none';\n            if(document.getElementById('share-theme-select')) document.getElementById('share-theme-select').disabled = true;")

# Re-enable the dropdown on modal close:
js = js.replace("document.getElementById('share-modal').style.display = 'none';",
                "document.getElementById('share-modal').style.display = 'none';\n            if(document.getElementById('share-theme-select')) document.getElementById('share-theme-select').disabled = false;")

# Also reset dropdown on open
js = js.replace("document.getElementById('share-modal').style.display = 'block';",
                "document.getElementById('share-modal').style.display = 'block';\n            if(document.getElementById('share-theme-select')) document.getElementById('share-theme-select').disabled = false;")


with open('src/static/app.js', 'w') as f:
    f.write(js)
