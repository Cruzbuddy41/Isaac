from flask import Flask, send_from_directory, jsonify
import os
import movement
import d5

app = Flask(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FLAG_FILE = os.path.join(CURRENT_DIR, 'stop.txt')

def clear_stop_flag():
    if os.path.exists(FLAG_FILE):
        os.remove(FLAG_FILE)

@app.route('/')
def index():
    return send_from_directory(CURRENT_DIR, 'hi.html', max_age=0)

@app.route('/img', methods=['POST'])
def serve_image():
    d5.takeImage()

@app.route('/move', methods=['POST'])
def move():
    clear_stop_flag()
    movement.move_forward(50, 1.0)
    return jsonify({"status": "success", "message": "Moved forward!"})

@app.route('/moveLeft', methods=['POST'])
def moveLeft():
    clear_stop_flag()
    movement.move_left(50, 1.0)
    return jsonify({"status": "success", "message": "Moved Left!"})

@app.route('/moveRight', methods=['POST'])
def moveRight():
    clear_stop_flag()
    movement.move_right(50, 1.0)
    return jsonify({"status": "success", "message": "Moved Right!"})

@app.route('/stop', methods=['POST'])
def stop():
    movement.stop_all()
    with open(FLAG_FILE, 'w') as f:
        f.write("stop")
    return jsonify({"status": "success", "message": "STOPPED!"})

@app.route('/resume', methods=['POST'])
def resume():
    clear_stop_flag()
    return jsonify({"status": "success", "message": "Resumed autonomous mode!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)