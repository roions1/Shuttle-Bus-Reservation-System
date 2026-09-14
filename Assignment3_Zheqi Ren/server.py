import socket
import threading

HOST = '127.0.0.1'
PORT = 3333
HEADER_LENGTH = 10

clients = {}
clients_lock = threading.Lock()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)#max 10 connections
print(f"Server started, listening on {HOST}:{PORT}")

#read exactly `length` bytes from socket, handles TCP partial reads
def recv_exact(sock, length):
    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            return None
        data += chunk
    return data

#read 10-byte header to get message length, then read the message body
def recv_msg(sock):
    header = recv_exact(sock, HEADER_LENGTH)
    if not header:
        return None
    length = int(header.decode().strip())
    data = recv_exact(sock, length)
    if not data:
        return None
    return data.decode()

#pack message: 10-byte fixed-length header (message size) + message body
def pack_msg(msg):
    encoded = msg.encode()
    header = f"{len(encoded):<{HEADER_LENGTH}}".encode()
    return header + encoded

#broadcast message to all clients except the sender
def broadcast(sender_sock, sender_name, message):
    packet = pack_msg(sender_name) + pack_msg(message)
    with clients_lock:
        for sock in list(clients):
            if sock != sender_sock:
                try:
                    sock.send(packet)
                except:
                    pass

#one thread per client, receives messages and broadcasts them
def handle_client(sock, addr):
    username = recv_msg(sock)
    if not username:
        sock.close()
        return
    with clients_lock:
        clients[sock] = username
    print(f"{username} connected from {addr}")
    while True:
        try:
            msg = recv_msg(sock)
            if not msg:
                break
            print(f"{username}: {msg}")
            broadcast(sock, username, msg)
        except:
            break
    with clients_lock:
        if sock in clients:
            del clients[sock]
    sock.close()
    print(f"{username} disconnected.")


while True:
    client_sock, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
    thread.start()