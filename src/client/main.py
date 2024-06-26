import sys
from tcpClient import TCPClient
from tlsClient import TLSClient

args = sys.argv[1:]
numArgs = len(args)
tcpClient = TCPClient()
tlsClient = TLSClient()

def __main__():
    """
    Main function for the wordlebot script.
    Accepts command line arguments and performs corresponding actions based on the arguments.

    Usage:
        ./main <server-hostname> [-p/--port port-number] [-s/--ssl issuer-name]

    Optional Parameters:
        -p/--port: Specify the port number for the connection. Default is 27993.
        -s/--ssl: Use SSL/TLS for the connection.

    Examples:
        python main.py example.com -p 12345
        python main.py example.com -s

    """
    if numArgs == 1 and (args[0] == "--help" or args[0] == "-h"):
        returnString = """
    Welcome to the wordlebot!
    To run the script, input commands in the following order...\n
        ./main <server-hostname> [-p/--port port-number] [-s/--ssl]\n
    If optional parameters are not passed, the default connection are port number 27993 with a standard TCP socket connection.
    Good luck and have fun with your personal wordle solver!
        """
        print(returnString)
    elif numArgs == 1:
        tcpClient.communicateTCP(args[0], 27993)
    elif numArgs == 2 and (args[1] == "-s" or args[1] == "--ssl"):
        tlsClient.communicateTLS(args[0], 27994)
    elif numArgs == 3 and (args[1] == "-p" or args[1] == "--port"):
        tcpClient.communicateTCP(args[0], int(args[2]))
    elif numArgs == 4 and (args[1] == "-p" or args[1] == "--port") and (args[3] == "-s" or args[3] == "--ssl"):
        tlsClient.communicateTLS(args[0], int(args[2]))
    else:
        argString = ""
        for arg in args:
            argString += arg + " "
        print("Invalid arguments: %s" % argString)

__main__()