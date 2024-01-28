### Libery
import socket
import select


### Config
server_ip = "localhost"
server_port = 12346
header_lenght = 999999


### Server Setting
client_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_connect.bind((server_ip, server_port))
client_connect.listen()
client_list = [client_connect]
clients = {}


### Functions
def receive_message(client_socket):# Functions - Receive Message
    try:
        message_header = client_socket.recv(header_lenght)
        if not len(message_header):
            return False
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return False


### Chat Room
print("Atomic Private Comunity - Chat Server")
while True:
    read_sockets, _, exception_sockets = select.select(client_list, [], client_list)
    for notified_socket in read_sockets:
        if notified_socket == client_connect:
            client_socket, client_address = client_connect.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            client_list.append(client_socket)
            clients[client_socket] = user
            print("Accepted new connection from {}:{}, username: {}".format(*client_address, user["data"].decode("utf-8")))
        else:
            message = receive_message(notified_socket)
            if message is False:
                print(f"Closed connection from: {clients[notified_socket]['data'].decode('utf-8')}")
                client_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])