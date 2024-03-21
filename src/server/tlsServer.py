import socket
import json
import ssl
from server import Server

class TLSServer(Server):
    """
    Represents a TLS server that listens for incoming connections and handles them using SSL/TLS encryption.

    Attributes:
        port (int): The port number on which the server listens for incoming connections.
        hostname (str): The hostname or IP address of the server.
    """

    port = 27994
    hostname = "127.0.0.1"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile='../../keys/certificate.crt', keyfile='../../keys/privateKey.key')
        s.bind((hostname, port))
        s.listen()
        sslSock = context.wrap_socket(sock=s, server_side=True)
        print("Socket connection opened and listening...")
        mysocket, addr = sslSock.accept()
        with mysocket:
            server = Server(mysocket)
            while True:
                data = json.loads(mysocket.recv(25600).decode())
                print(data)
                if server.typeParser(data) == False:
                    break  
            mysocket.shutdown(socket.SHUT_RDWR)
            mysocket.close()
        s.close()