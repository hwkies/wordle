import socket
from client import Client

class TCPClient(Client):
    """
    A client class for communicating with a TCP server.
    """

    def communicateTCP(self, hostname, port):
        """
        Communicates with a TCP server.

        Args:
            hostname (str): The hostname of the server.
            port (int): The port number of the server.

        Returns:
            None
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dataHandler(client, hostname, port)