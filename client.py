import socket
import threading

HOST = '127.0.0.1'
PORT = 3333
HEADER_LENGTH = 10

username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
#send username immediately after connecting so server can identify this client
encoded = username.encode()
header = f"{len(encoded):<{HEADER_LENGTH}}".encode()
client_socket.send(header + encoded)


def recv_exact(sock, length):
    #length` bytes from socket, handles TCP partial reads
    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            return None
        data += chunk
    return data


def receive():
    #continuously receive and print broadcast messages from server
    while True:
        try:
            sender_header = recv_exact(client_socket, HEADER_LENGTH)
            if not sender_header:
                break
            sender_len = int(sender_header.decode().strip())
            sender = recv_exact(client_socket, sender_len).decode()

            msg_header = recv_exact(client_socket, HEADER_LENGTH)
            if not msg_header:
                break
            msg_len = int(msg_header.decode().strip())
            msg = recv_exact(client_socket, msg_len).decode()

            print(f"\n{sender} > {msg}")
        except:
            print("Disconnected from server.")
            break


receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

while True:
    msg = input(f"{username} > ")
    if msg:
        encoded = msg.encode()
        header = f"{len(encoded):<{HEADER_LENGTH}}".encode()
        client_socket.send(header + encoded)