import re

with open('src/templates/share.html', 'r') as f:
    html = f.read()

replacement_css = """
  :root {
    --bg-color: #1e1e1e; /* Dark (default) */
    --text-color: #cccccc;
  }
  body.theme-light {
    --bg-color: #ffffff;
    --text-color: #333333; /* Dark Grey text */
  }
  body.theme-dark {
    --bg-color: #1e1e1e; /* Dark Grey background */
    --text-color: #cccccc; /* Light Grey text */
  }
  body.theme-full {
    --bg-color: #1e1e1e;
    --text-color: #cccccc;
  }
  body {
    background-color: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    padding: 0;
    font-family: 'Courier New', Courier, monospace;
    display: flex;
    justify-content: center;
    box-sizing: border-box;
    min-height: 100vh;
  }
  .terminal-wrapper {
    width: 100%;
    /* No max-width, make it full screen */
    background-color: var(--bg-color);
    padding: 10px;
    box-sizing: border-box;
    overflow-x: auto;
  }
"""

html = re.sub(r':root \{.*?\.terminal-wrapper \{.*?\}', replacement_css.strip() + "\n", html, flags=re.DOTALL)
html = re.sub(r'\.terminal-wrapper pre, \.terminal-wrapper div \{', '.terminal-wrapper pre, .terminal-wrapper div {\n    margin: 0;\n    padding: 0;\n    box-sizing: border-box;\n    font-family: inherit;\n    line-height: 1.2;\n}', html)

with open('src/templates/share.html', 'w') as f:
    f.write(html)
