with open("tests/test_e2e_csrf_upload.py", "r") as f:
    content = f.read()

# Capture console logs
console_capture = """
        upload_requests = []
        page.on("request", lambda request: upload_requests.append(request) if "/api/upload" in request.url else None)
        
        # Capture console messages
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
"""

content = content.replace('        upload_requests = []\n        page.on("request", lambda request: upload_requests.append(request) if "/api/upload" in request.url else None)', console_capture)

with open("tests/test_e2e_csrf_upload.py", "w") as f:
    f.write(content)
