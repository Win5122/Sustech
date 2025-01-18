from flask import Flask
import signal
import sys
import os

app = Flask(__name__)

@app.route('/')
def hello():
    pod_name = os.getenv('POD_NAME', 'unknown')
    pod_ip = os.getenv('POD_IP', 'unknown')
    node_name = os.getenv('NODE_NAME', 'unknown')
    return f"Hello from {pod_name}, IP: {pod_ip}, Node: {node_name}\n"

@app.route('/chat/<username>')
def greet_with_info(username):
    return f"Hello {username}, welcome to the Flask app!\n"

def graceful_shutdown(signum, frame):
    print("Gracefully shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('FLASK_PORT', 5000)))
    signal.signal(signal.SIGTERM, graceful_shutdown)
