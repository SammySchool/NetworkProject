import socket

class Network:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = 'localhost'
        self.PORT = 9090
        self.addr = (self.HOST, self.PORT)
        self.pos = self.connect()
    
    def get_pos(self):
        return self.pos
    
    def connect(self):
        try:
            self.client_socket.connect(self.addr)
            return self.client_socket.recv(2048).decode('utf-8')
        except:
            pass

    def send(self, data):
        try:
            self.client_socket.send(str.encode(data))
            return self.client_socket.recv(2048).decode('utf-8')
        except socket.error as e:
            print(e)
