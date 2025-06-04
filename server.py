from flask import Flask, request, jsonify
from datetime import datetime
import sys

app = Flask(__name__)

@app.route('/ping', methods=['POST'])
def ping():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Нет JSON в запросе'}), 400

    packet_id = data.get('packet_id')
    master_send_time = data.get('master_send_time')
    client_id = data.get('client_id', 'anonymous')

    # Время приема на сервере
    slave_recv_time = int(datetime.utcnow().timestamp() * 1000)

    # IP клиента (из заголовков или из remote_addr)
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Логируем с flush=True, чтобы сразу увидеть в логах
    print(f"[{datetime.utcnow():%Y-%m-%d %H:%M:%S.%f}] "
          f"Получен пакет #{packet_id} от клиента '{client_id}' (IP: {client_ip}), "
          f"server_receive={slave_recv_time}", flush=True)

    # Возвращаем время приема на сервере
    return jsonify({'serverTime': slave_recv_time})

if __name__ == '__main__':
    # Запускаем на 0.0.0.0:10000, чтобы был доступ снаружи
    app.run(host='0.0.0.0', port=10000)
