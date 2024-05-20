# network.py
import socket

class Network:
    def __init__(self):
        self.connections = []

    def connect(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            self.connections.append(s)
            return f"Connected to {host}:{port}."
        except socket.error as e:
            return f"Connection error: {e}"

    def send(self, connection_index, message):
        try:
            self.connections[connection_index].sendall(message.encode())
            return "Message sent."
        except IndexError:
            return "Invalid connection index."
        except socket.error as e:
            return f"Error sending message: {e}"
