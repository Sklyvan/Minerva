import socket

class SocketConnection:
    def __init__(self, toIP='127.0.0.1', throughPort=6774):
        """
        This class is used to connect to a socket and transfer the data.
        The data should be in bytes, in case it is not, it will be converted to bytes.
        This is used to send the already created NetworkMessage as bytes to JavaScript.
        :param toIP: The IP to open the socket, by default is the localhost.
        :param throughPort: The port where the socket will be opened, by default is 8080.
        """
        self.HOST = toIP
        self.PORT = throughPort
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isOpen = False

    def start(self):
        self.clientSocket.connect((self.HOST, self.PORT))
        self.isOpen = True

    def close(self):
        self.clientSocket.close()
        self.isOpen = False

    def send(self, data):
        self.clientSocket.sendall(data)

    def __str__(self):
        return f"SocketConnection to {self.HOST}:{self.PORT}"

    def __repr__(self):
        return f"SocketConnection to {self.HOST}:{self.PORT}"

    def __del__(self):
        self.close()
