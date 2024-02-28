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

