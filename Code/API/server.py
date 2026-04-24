from flask import Flask, send_from_directory, jsonify, send_file
import os
import movement
import d4
import the_robot_photo

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FLAG_FILE = os.path.join(BASE_DIR, 'stop.txt')


def is_stopped():
    return os.path.exists(FLAG_FILE)

with open(FLAG_FILE, 'w') as f: f.write("stop")


@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'hi.html')

@app.route('/img', methods=['POST'])
def process_frame():
    img, direction = d4.takeImage()

    if not is_stopped():
        d4.apply_movement(direction)
        status_msg = f"Auto-driving: {direction}"
    else:
        status_msg = "Manual mode (Visuals only)"

    return jsonify({"status": "success", "message": status_msg})


@app.route('/get_processed_image')
def get_image():
    return send_file(os.path.join(BASE_DIR, 'lanes_result.jpg'), max_age=0)


@app.route('/move', methods=['POST'])
def move_manual():
    movement.move_forward(50, 1.0)
    return jsonify({"status": "success", "message": "Manual Forward"})

@app.route('/moveLeft', methods=['POST'])
def move_left_manual():
    movement.move_left(50, 1.0)
    return jsonify({"status": "success", "message": "Manual Left"})

@app.route('/moveRight', methods=['POST'])
def move_right_manual():
    movement.move_right(50, 1.0)
    return jsonify({"status": "success", "message": "Manual Right"})

@app.route('/stop', methods=['POST'])
def stop():
    movement.stop_all()
    with open(FLAG_FILE, 'w') as f: f.write("stop")
    return jsonify({"status": "success"})


@app.route('/resume', methods=['POST'])
def resume():
    if os.path.exists(FLAG_FILE):
        os.remove(FLAG_FILE)
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)