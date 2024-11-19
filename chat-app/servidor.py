import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            break

def broadcast(message, current_client):
    for client in clients:
        if client != current_client:
            client.send(message.encode('utf-8'))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5555))
server.listen()

clients = []
print("Servidor rodando...")

while True:
    client_socket, client_address = server.accept()
    print(f"Conectado com {client_address}!")
    clients.append(client_socket)
    
    threading.Thread(target=handle_client, args=(client_socket,)).start()
