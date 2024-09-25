import socket

# IP adresi ve port numarası
ip_address = '127.0.0.1'
port = 65432

# Dosya yolu
file_path = "isa.bin"

# TCP bağlantısı aç
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((ip_address, port))
    
    # Dosyayı aç ve 54 baytlık bloklar halinde oku
    with open(file_path, "rb") as file:
        while True:
            # 54 bayt oku
            data = file.read(54)
            
            # Dosyanın sonuna gelindiyse döngüyü bitir
            if not data:
                break
            
            # Okunan veriyi TCP üzerinden gönder
            sock.sendall(data)
            
            # Gönderilen veriyi hex olarak konsola bas
            print(f"Gönderilen veri (hex): {data.hex()}")            
            # Sunucudan cevap al
            response = sock.recv(1024)  # 1024 bayt kadar cevap alabilir
            print(f"Sunucudan gelen cevap: {response.decode()}")
