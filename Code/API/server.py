from flask import Flask, send_from_directory, jsonify, send_file
import os
import movement

app = Flask(__name__)
DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_from_directory(DIR, 'hi.html')

@app.route('/lanes_result.jpg')
def get_image():
    # Browser will call this to see the latest image + triangles
    return send_file(os.path.join(DIR, 'lanes_result.jpg'), mimetype='image/jpeg')

@app.route('/get_log')
def get_log():
    # Browser will call this to see the text status
    try:
        with open(os.path.join(DIR, 'log.txt'), 'r') as f:
            return jsonify({"status": f.read()})
    except:
        return jsonify({"status": "Waiting..."})

# Manual Overrides (Buttons)
@app.route('/stop', methods=['POST'])
def stop():
    with open(os.path.join(DIR, 'stop.txt'), 'w') as f: f.write("stop")
    movement.stop_all()
    return jsonify({"status": "locked"})

@app.route('/resume', methods=['POST'])
def resume():
    if os.path.exists(os.path.join(DIR, 'stop.txt')):
        os.remove(os.path.join(DIR, 'stop.txt'))
    return jsonify({"status": "resumed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)