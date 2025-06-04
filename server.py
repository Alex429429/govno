from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

def get_client_ip():
    if "X-Forwarded-For" in request.headers:
        # Берём первый IP из списка X-Forwarded-For
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

    client_id = data.get('client_id', client_ip)
    packet_id = data.get('packet_id')
    master_send_time = data.get('master_send_time')

    # Время приёма сервером (slave time) в миллисекундах UTC
    slave_recv_time = int(datetime.utcnow().timestamp() * 1000)

    response = {
        'client_id': client_id,
        'packet_id': packet_id,
        'slave_recv_time': slave_recv_time,
        'slave_send_time': slave_recv_time
    }

    print(f"Received from {client_id} (IP {client_ip}): packet #{packet_id} at slave_recv_time={slave_recv_time}")
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
