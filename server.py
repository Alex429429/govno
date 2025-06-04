from flask import Flask, request, jsonify
import time
import os

app = Flask(__name__)

@app.route('/ping', methods=['POST'])
def ping():
    slave_receive_time = int(time.time() * 1000)

    data = request.json or {}
    packet_id = data.get('packet_id')
    master_send_time = data.get('master_send_time')

    # Возвращаем в ответе время приема пакета на сервере, без использования локального времени отправки
    return jsonify({
        'packet_id': packet_id,
        'master_send_time': master_send_time,
        'slave_receive_time': slave_receive_time
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
