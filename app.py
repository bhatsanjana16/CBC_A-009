from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

process = None  # To track the running process

@app.route('/')
def index():
    return render_template('index.html')  # Your frontend page

@app.route('/start', methods=['POST'])
def start_main():
    global process
    if process is None:
        process = subprocess.Popen(["python", "main.py"])
        return jsonify({"status": "started"})
    return jsonify({"status": "already running"})

@app.route('/stop', methods=['POST'])
def stop_main():
    global process
    if process is not None:
        process.terminate()
        process = None
        return jsonify({"status": "stopped"})
    return jsonify({"status": "not running"})

if __name__ == '__main__':
    app.run(debug=True)



