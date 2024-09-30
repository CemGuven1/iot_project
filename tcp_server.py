import socket
import struct
import requests
import json
import time

# Django API endpoint (replace with your actual endpoint)
API_URL = 'http://localhost:8000/api/data-entry/'  # Change this URL

def post_to_django(data):
    """Send the parsed data to the Django app via a POST request."""
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(API_URL, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("Data successfully posted to Django.")
        else:
            print(f"Failed to post data: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending data to Django: {e}")

def parse_device_data(binary_data):
    """Parse the 54-byte binary data received from the client."""
    format_str = '<H I I H B i i i h h h h h h h h 6h B'  # Little-endian format
    unpacked_data = struct.unpack(format_str, binary_data)

    # Create a dictionary with parsed values
    parsed_data = {
        'device_id': unpacked_data[0],
        'packetID': unpacked_data[1],
        'unix_time': unpacked_data[2],
        'millisecond': unpacked_data[3],
        'acceleration_x': unpacked_data[5],  # ADXL AccX
        'acceleration_y': unpacked_data[6],  # ADXL AccY
        'acceleration_z': unpacked_data[7],  # ADXL AccZ
        'gyro_x': unpacked_data[12],         # LSM6 GyroX
        'gyro_y': unpacked_data[13],         # LSM6 GyroY
        'gyro_z': unpacked_data[14],         # LSM6 GyroZ
        'temperature': unpacked_data[8],     # ADXL Temp
        'battery': 100
    }
    return parsed_data

def start_tcp_server():
    """Start the TCP server to receive data from IoT clients."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse the port if needed
    server_socket.bind(('0.0.0.0', 65432))  # Bind to all interfaces on port 65432
    server_socket.listen(5)
    
    print("TCP server listening on port 65432...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        try:
            while True:  # Keep receiving data from the client
                # Receive 54 bytes of binary data from the client
                data = client_socket.recv(54)
                
                if len(data) == 54:
                    print(f"Received {len(data)} bytes of data.")
                    
                    try:
                        # Parse the binary data
                        parsed_data = parse_device_data(data)
                        print(f"Parsed data: {parsed_data}")
                        
                        # Post parsed data to Django
                        post_to_django(parsed_data)
                        
                    except struct.error as e:
                        print(f"Error unpacking data: {e}")
                elif len(data) == 0:
                    # No more data, client likely closed the connection
                    print("Client closed the connection.")
                    break
                else:
                    print(f"Received incomplete data: {len(data)} bytes")
        
        except Exception as e:
            print(f"Error during client communication: {e}")
        
        client_socket.close()
        print(f"Connection with {addr} closed.")

if __name__ == "__main__":
    start_tcp_server()
