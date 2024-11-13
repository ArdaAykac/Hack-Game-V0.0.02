import socket
import threading

clients = []

def handle_client(client_socket):
    try:
        # Bağlantı kurulduktan sonra istemciye hoş geldiniz mesajı gönder
        client_socket.send("Hoş geldiniz! Sunucuya başarıyla bağlandınız.\n".encode())
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            client_socket.send(f"Sunucuya gönderilen mesaj: {data.decode()}\n".encode())
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))  # Port 12345'i dinle
    server_socket.listen(5)
    print("Sunucu başlatıldı. Bağlantılar bekleniyor...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"{client_address} bağlantısı kabul edildi.")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    start_server()
