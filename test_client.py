import socket
import json
import time
from datetime import datetime

def send_data_to_server(data):
    """Send data to the TCP server."""
    server_ip = '127.0.0.1'  # Replace with the actual IP if needed
    server_port = 65432
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    message = json.dumps(data)
    client_socket.send(message.encode('utf-8'))
    print(f"Sent data: {data}")
    
    client_socket.close()

if __name__ == "__main__":
    # Simulate sending device data every few seconds
    for i in range(10):
        simulated_data = {
            'packetID': '12345678',
            'device_id': '123123123',
            'acceleration_x': i * 0.1,
            'acceleration_y': i * 0.2,
            'acceleration_z': i * 0.3,
            'gyro_x': i * 0.01,
            'gyro_y': i * 0.02,
            'gyro_z': i * 0.03,
            'temperature': 25 + i * 0.5,
            'battery': 100 - i * 2
        }
        send_data_to_server(simulated_data)
        time.sleep(5)  # Wait before sending the next data
