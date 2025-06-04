from flask import Flask, jsonify
import time
import os

app = Flask(__name__)

@app.route('/ping')
def ping():
    server_time = int(time.time() * 1000)
    return jsonify({'serverTime': server_time})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
