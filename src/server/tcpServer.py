import socket
import json
from server import Server

class TCPServer(Server):
    """
    Represents a TCP server that listens for incoming connections and handles data communication.

    Attributes:
        port (int): The port number to listen on.
        hostname (str): The hostname or IP address to bind the server to.
    """

    port = 27993
    hostname = "127.0.0.1"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((hostname, port))
        s.listen()
        print("Socket connection opened and listening...")
        mysocket, addr = s.accept()
        with mysocket:
            server = Server(mysocket)
            while True:
                data = json.loads(mysocket.recv(25600).decode())
                if server.typeParser(data) == False:
                    break  
            mysocket.shutdown(socket.SHUT_RDWR)
            mysocket.close()
        s.close()