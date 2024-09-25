import socket
import requests
import json
import struct
import datetime

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
        
        ###data = client_socket.recv(1024).decode('utf-8')
        ###print(f"Received data: {data}")
        
        # Receive 54 bytes of hex data
        data = client_socket.recv(54)
        if not data:
            break
        
        # Parse the received data
        simulated_data = parse_received_data(data)
        print("Simulated Data:", json.dumps(simulated_data, indent=2))
        
        
        # Assuming data is JSON encoded from the IoT device
        try:
            parsed_data = json.loads(data)
            print(f"Parsed data: {parsed_data}")
            ##post_to_django(parsed_data)
        except json.JSONDecodeError as e:
            print(f"Failed to parse data: {e}")
        
        client_socket.close()




def parse_received_data(data):
    # Ensure the data is exactly 54 bytes
    if len(data) != 54:
        raise ValueError("Received data must be exactly 54 bytes.")

    # Unpack the data based on the expected structure
    # Assuming you received: Opcode, DeviceId, PacketId, UnixTime, Millisecond, SensorInfo, AccX, AccY, AccZ, Temp, etc.

    # Example unpacking based on the structure you provided
    Opcode = data[0]
    DeviceId = struct.unpack('<H', data[1:3])[0]  # 2 bytes
    PacketId = struct.unpack('<I', data[3:7])[0]  # 4 
    
    
    UnixTime = struct.unpack('<I', data[7:11])[0]  # 4 bytes
    # Convert to datetime
    dt = datetime.datetime.fromtimestamp(UnixTime)
    Millisecond = struct.unpack('<H', data[11:13])[0]  # 2 bytes
    # Add milliseconds using timedelta
    dt_with_ms = dt + datetime.timedelta(milliseconds=Millisecond)


    SensorInfo = data[13]
    
    # Assuming AccX, AccY, AccZ data format as specified (example)
    AccX = [data[14], data[15], data[16]]  # 3 bytes
    AccY = [data[17], data[18], data[19]]  # 3 bytes
    AccZ = [data[20], data[21], data[22]]  # 3 bytes
    Temp = data[23:25]  # 2 bytes for temperature
    # Additional fields can be extracted similarly...

    # Example: convert AccX, AccY, AccZ to float values (you'll need actual conversion logic)
    accel_x = sum(AccX) / 3.0  # Placeholder logic
    accel_y = sum(AccY) / 3.0  # Placeholder logic
    accel_z = sum(AccZ) / 3.0  # Placeholder logic

    # Create the simulated data dictionary
    simulated_data = {
        'device_id': DeviceId,
        "timestamp": dt_with_ms,
        "temperature": struct.unpack('<H', Temp)[0],
        "accel_x": accel_x,
        "accel_y": accel_y,
        "accel_z": accel_z,
        "gyro_x": 0.01,  # Replace with actual gyro calculation
        "gyro_y": 0.02,  # Replace with actual gyro calculation
        "gyro_z": 0.03,  # Replace with actual gyro calculation
        "battery": 100 - (PacketId % 100)
    }

    return simulated_data



if __name__ == "__main__":
    start_tcp_server()
