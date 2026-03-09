import re

with open("tests/test_e2e_csrf_upload.py", "r") as f:
    content = f.read()

# Add a step to corrupt the token right before upload
corrupt_step = """
        # Corrupt the token right before upload to simulate token expiration
        page.evaluate('''() => {
            const meta = document.querySelector('meta[name="csrf-token"]');
            if (meta) meta.setAttribute('content', 'token_expired_123');
        }''')
        
        page.once("dialog", lambda dialog: dialog.accept())
"""

content = content.replace('page.once("dialog", lambda dialog: dialog.accept())', corrupt_step)

with open("tests/test_e2e_csrf_upload.py", "w") as f:
    f.write(content)
