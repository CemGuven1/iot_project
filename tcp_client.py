import socket
import time

# IP & Port
ip_address = '127.0.0.1'
port = 65432

# Data folder
file_path = "data.bin"

# TCP Connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((ip_address, port))
    
    # Open folder
    with open(file_path, "rb") as file:
        while True:
            # read 54 byrte 
            data = file.read(54)
            
            # End loop file end
            if not data:
                break
            
            # Send data through TCP
            sock.sendall(data)
            print(f"sent data (hex): {data.hex()}")      
