from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Lock
import math
import random
import time
from datetime import datetime
from threading import Thread

# The Mock Data Generator (Sine Wave)
class MockSensor:
    def __init__(self):
        self.t = 0

    def get_data(self):
        # Increment time to create movement
        self.t += 0.5
        
        # Generate Sine Wave: sin(t) * amplitude + offset
        # This creates a predictable wave pattern between 40 and 60
        base_value = math.sin(self.t) * 10 + 50
        
        # Add random jitter (simulating sensor noise)
        noise = random.uniform(-2, 2)
        
        final_value = round(base_value + noise, 2)
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        return {'x': timestamp, 'y': final_value}
    

# Setup the flask web framework with socketio.
app = Flask(__name__)
app.config['SECRET_KEY'] = "9876543210"
socketio = SocketIO(app, async_mode="threading")

# Prevents multiple threads from starting if you open multiple tabs.
thread = None
thread_lock = Lock()

# Initialize the sensor.
sensor = MockSensor()

# 4. Background Thread Function
def background_thread():
    """Sends data to the client every 0.5 seconds"""
    while True:
        # Adjust this sleep time to control refresh rate
        # 0.1 = Fast (100ms), 1.0 = Slow (1s)
        time.sleep(0.5)
        
        data = sensor.get_data()
        
        # emit() sends the data to the javascript frontend
        socketio.emit('update_graph', data)

# Flask WebApp Routes.
@app.route("/")
def home():
    return render_template("index.html")

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            # Start the background thread only if it isn't running yet
            thread = socketio.start_background_task(background_thread)
            print("Client connected: Background thread started.")

@socketio.event
def disconnect():
    print("Client disconnected")

if __name__ == "__main__":
    socketio.run(app, debug=True)