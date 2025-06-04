from flask import Flask, request, jsonify
from datetime import datetime
import os
import time

app = Flask(__name__)

def get_client_ip():
    # Попытка достать реальный IP из заголовков (Render/прокси)
    if "X-Forwarded-For" in request.headers:
        return request.headers["X-Forwarded-For"].split(",")[0].strip()
    elif "X-Real-IP" in request.headers:
        return request.headers["X-Real-IP"]
    else:
        return request.remote_addr

@app.route('/ping', methods=['POST'])
def ping():
    client_ip = get_client_ip()
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON received'}), 400

    # Берём nick (client_id) из запроса; если не передали – подставляем IP
    client_id = data.get('client_id', client_ip)
    packet_id = data.get('packet_id')
    master_send_time = data.get('master_send_time')

    # Зафиксируем, когда сервер принял пакет (UTC в миллисекундах)
    slave_recv_time = int(time.time() * 1000)
    # Сейчас же отправляем ответ, пусть slave_send_time совпадает с recv
    slave_send_time = slave_recv_time

    # Логируем в консоль (Render → Logs)
    print(f"[{datetime.utcnow():%Y-%m-%d %H:%M:%S.%f}] "
          f"Получен пакет #{packet_id} от клиента '{client_id}' (IP: {client_ip}), "
          f"server_receive={slave_recv_time}")

    # Формируем JSON-ответ
    return jsonify({
        'client_id': client_id,
        'packet_id': packet_id,
        'slave_recv_time': slave_recv_time,
        'slave_send_time': slave_send_time
    }), 200

if __name__ == '__main__':
    # Render задаёт порт в переменной окружения PORT
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
