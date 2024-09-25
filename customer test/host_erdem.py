import socket
import os
import threading
from datetime import datetime


def handle_client(client_socket, client_address):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data
        with open("messages.txt", "a") as f:
            f.write(f"{datetime.now()} {client_address}: {message}\n\n")
        print(f"Message from {client_address}: {message}")
        response = "Server received your message."
        client_socket.sendall(response.encode('utf-8'))
    client_socket.close()
    
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '127.0.0.1'
    port = 65432
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()