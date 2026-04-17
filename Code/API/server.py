from flask import Flask, send_from_directory, jsonify
import os
import movement

app = Flask(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_from_directory(CURRENT_DIR, 'hi.html')

@app.route('/lanes_result.jpg')
def serve_image():
    return send_from_directory(CURRENT_DIR, 'lanes_result.jpg')

@app.route('/move', methods=['POST'])
def move():
    movement.move_forward(50,1.0)
    return jsonify({"status": "success", "message": "Moved forward!"})

@app.route('/moveLeft', methods=['POST'])
def moveLeft():
    movement.move_left(50,1.0)
    return jsonify({"status": "success", "message": "Moved Left!"})

@app.route('/moveRight', methods=['POST'])
def moveRight():
    movement.move_right(50,1.0)
    return jsonify({"status": "success", "message": "Moved Right!"})

@app.route('/stop', methods=['POST'])
def stop():
    movement.stop_all()
    return jsonify({"status": "success", "message": "STOPPED!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)