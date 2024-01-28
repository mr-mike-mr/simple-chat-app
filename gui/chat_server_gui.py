### Libery
import socket
import threading


### Config
server_ip = "localhost"
server_port = 12346
header_lenght = 999999

### Premenné
clients = []


### Functions
# brodcast message
def broadcast_message(message):
    for client in clients:
        client.send(message.encode('utf-8'))
# client hanfle
def handle_client(client_socket, address):
    clients.append(client_socket)
    while True:
        data = client_socket.recv(header_lenght).decode('utf-8')
        if not data:
            break
        broadcast_message(data)
    clients.remove(client_socket)
    client_socket.close()
# server start
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()


### Chat Room
print("Atomic Private Comunity - Chat Server")
start_server()