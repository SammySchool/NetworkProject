import socket
import threading
import time
import sys

HOST = 'localhost'
PORT = 9090

MAX_PLAYERS = 2

players = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))
    sys.exit()

server_socket.listen(2)
print(f'Server is listening on port {PORT}')

def handle_client(client_socket, player_name):
    while len(players) < MAX_PLAYERS:
        client_socket.send('Waiting for other players to join...'.encode('utf-8'))
        time.sleep(1)
    client_socket.send('Game is starting...'.encode('utf-8'))
    client_socket.close()

while True:
    client_socket, addr = server_socket.accept()
    print(f'Connection from {addr} has been established!')
    player_name = client_socket.recv(1024).decode('utf-8')
    players.append(player_name)
    thread = threading.Thread(target=handle_client, args=(client_socket, player_name))
    thread.start()

server_socket.close()

# Path: client.py
import socket

HOST = 'localhost'
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

player_name = input('Enter your name: ')
client_socket.send(player_name.encode('utf-8'))

while True:
    message = client_socket.recv(1024).decode('utf-8')
    print(message)
    if message == 'Game is starting...':
        break
    
client_socket.close()

#The server will accept connections from clients and store their names in a list. Once the list has two names, the server will start the game. The client will send their name to the server and wait for the game to start. Once the game starts, the client will close the connection.


