from flask import Flask, request, jsonify
import time
import os
from datetime import datetime

app = Flask(__name__)

def format_time(ms):
    return datetime.fromtimestamp(ms / 1000).strftime('%H:%M:%S.%f')[:-3]

@app.route('/ping', methods=['POST'])
def ping():
    slave_receive_time = int(time.time() * 1000)

    data = request.json or {}
    packet_id = data.get('packet_id')
    master_send_time = data.get('master_send_time')

    slave_send_time = int(time.time() * 1000)

    # 🧾 Отладка в консоли Render
    print(f"\n📦 Пакет #{packet_id}")
    print(f"  Время отправки мастером:     {format_time(master_send_time)}")
    print(f"  Время приёма на слейве:      {format_time(slave_receive_time)}")
    print(f"  Время отправки с слейва:     {format_time(slave_send_time)}")

    return jsonify({
        'packet_id': packet_id,
        'master_send_time': master_send_time,
        'slave_receive_time': slave_receive_time,
        'slave_send_time': slave_send_time
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
