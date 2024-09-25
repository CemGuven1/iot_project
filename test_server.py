import socket
import requests
import json

# Django API endpoint (replace with your actual endpoint)
API_URL = 'http://localhost:8000/api/data-entry/'  # Change this URL

def post_to_django(data):
    """Send the parsed data to the Django app via a POST request."""
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(API_URL, data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            print("Data successfully posted to Django.")
        else:
            print(f"Failed to post data: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending data to Django: {e}")

def start_tcp_server():
    """Start the TCP server to receive data from IoT clients."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 65432))  # Bind to all interfaces on port 65432
    server_socket.listen(5)
    
    print("TCP server listening on port 65432...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received data: {data}")
        
        # Assuming data is JSON encoded from the IoT device
        try:
            parsed_data = json.loads(data)
            print(f"Parsed data: {parsed_data}")
            post_to_django(parsed_data)
        except json.JSONDecodeError as e:
            print(f"Failed to parse data: {e}")
        
        client_socket.close()

if __name__ == "__main__":
    start_tcp_server()