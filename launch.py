import subprocess
import webbrowser
import time
import sys
import signal

# Step 1: Start Flask app (main.py)
server = subprocess.Popen([sys.executable, "main.py"])

# Step 2: Wait a bit for the server to start
time.sleep(2)

# Step 3: Open browser only once
webbrowser.open_new("http://127.0.0.1:5000")

# Step 4: Keep running until user closes
try:
    server.wait()
except KeyboardInterrupt:
    server.send_signal(signal.SIGTERM)
    server.terminate()
