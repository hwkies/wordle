import socket
import ssl
from client import Client

class TLSClient(Client):
    #create a TLS encrypted client to send and receive data
    def communicateTLS(self, hostname, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context()
        encryptclient = context.wrap_socket(client, server_hostname=hostname)
        self.dataHandler(encryptclient, hostname, port)