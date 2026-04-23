from flask import Flask, send_from_directory, jsonify
import os
import movement
import d4  # Ensure this is d4

app = Flask(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FLAG_FILE = os.path.join(CURRENT_DIR, 'stop.txt')

def clear_stop_flag():
    if os.path.exists(FLAG_FILE):
        os.remove(FLAG_FILE)

def set_stop_flag():
    with open(FLAG_FILE, 'w') as f:
        f.write("stop")

# --- INITIALIZE STOP STATE ON STARTUP ---
set_stop_flag() 

@app.route('/')
def index():
    return send_from_directory(CURRENT_DIR, 'hi.html', max_age=0)

@app.route('/img', methods=['POST'])
def serve_image():
    # Only processes if called; d4 loop handles the 'live' logic
    d4.takeImage()
    return jsonify({"status": "success", "message": "Image captured"})

@app.route('/get_processed_image')
def get_processed_image():
    return send_from_directory(CURRENT_DIR, 'lanes_result.jpg', max_age=0)

@app.route('/move', methods=['POST'])
def move():
    # REMOVED clear_stop_flag() so autonomous stays off
    movement.move_forward(50, 1.0)
    return jsonify({"status": "success", "message": "Manual Move forward!"})

@app.route('/moveLeft', methods=['POST'])
def moveLeft():
    movement.move_left(50, 1.0)
    return jsonify({"status": "success", "message": "Manual Move Left!"})

@app.route('/moveRight', methods=['POST'])
def moveRight():
    movement.move_right(50, 1.0)
    return jsonify({"status": "success", "message": "Manual Move Right!"})

@app.route('/stop', methods=['POST'])
def stop():
    movement.stop_all()
    set_stop_flag()
    return jsonify({"status": "success", "message": "STOPPED!"})

@app.route('/resume', methods=['POST'])
def resume():
    # This is the ONLY button that enables autonomous mode
    clear_stop_flag()
    return jsonify({"status": "success", "message": "Resumed autonomous mode!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)