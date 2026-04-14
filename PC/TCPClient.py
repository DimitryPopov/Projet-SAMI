import socket

class TCPClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self, host, port):
        self.sock.connect((host, port))
    def send(self, msg):
        self.sock.send(msg.encode())

    def receive(self):
        received_msg = self.sock.recv(1024)
        print(received_msg.decode())
        return received_msg
    def close(self):
        self.sock.close()