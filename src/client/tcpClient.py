import socket
from client import Client

class TCPClient(Client):
    #create a TCP client and send to receive data
    def communicateTCP(self, hostname, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect to the server with the specified hostname and port
        self.dataHandler(client, hostname, port)