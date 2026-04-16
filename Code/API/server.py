from flask import Flask, send_from_directory, jsonify
import os
import movement

app = Flask(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_from_directory(CURRENT_DIR, 'index.html')

@app.route('/lanes_result.jpg')
def serve_image():
    return send_from_directory(CURRENT_DIR, 'lanes_result.jpg')

@app.route('/move', methods=['POST'])
def move():
    movement.move_forward(50,1.0)  # This executes your imported Python function
    return jsonify({"status": "success", "message": "Moved forward!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)