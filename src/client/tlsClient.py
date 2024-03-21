import socket
import ssl
from client import Client

class TLSClient(Client):
    """A class representing a TLS encrypted client to send and receive data."""

    def communicateTLS(self, hostname, port):
        """
        Establishes a TLS connection with the specified hostname and port.

        Args:
            hostname (str): The hostname of the server.
            port (int): The port number to connect to.

        Returns:
            None
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context()
        context.check_hostname = False
        encryptclient = context.wrap_socket(client, server_hostname=hostname)
        self.dataHandler(encryptclient, hostname, port)