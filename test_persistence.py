import requests
import time
import json
import subprocess
import os

# start server
proc = subprocess.Popen(['python3', 'src/app.py'], env=dict(os.environ, GEMINI_TEST_PORT='5055'))
time.sleep(3)

# make local sessions
for i in range(10):
    subprocess.run(['python3', 'src/fake_gemini.py', f'--name=session_{i}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    s = requests.Session()
    # first fetch with cache=false, bg=true
    r = s.get('http://127.0.0.1:5000/api/sessions?bg=true')
    print("First fetch:", r.json())
    time.sleep(1)
    
    r2 = s.get('http://127.0.0.1:5000/api/sessions?bg=true&cache=true')
    print("Second fetch (cache):", r2.json())
    
finally:
    proc.terminate()
