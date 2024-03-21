import json
import sys
sys.path.append('..')
import utils

class Server:
    """
    Represents a server for the Wordle game.

    Attributes:
        mysocket (socket): The socket object for communication.
        util (utils.Utils): An instance of the Utils class.
        answer (str): The randomly generated word to be guessed.
        guessList (list): A list of dictionaries representing the guesses made by the client.

    Methods:
        __init__(self, sock): Initializes the Server object.
        typeParser(self, msg): Parses the message received from the client and performs the corresponding actions.
        sendStart(self): Sends the start message to the client.
        guessNotInList(self): Sends a retry message to the client when the guessed word is not in the wordlist.
        wrongGuess(self, guess): Handles the case when the guessed word is incorrect.
        correctGuess(self): Handles the case when the guessed word is correct.
    """

    mysocket = None
    util = utils.Utils()
    answer = util.getRandWord()
    guessList = []

    def __init__(self, sock):
        self.mysocket = sock

    def typeParser(self, msg):
        """
        Parses the message type and performs corresponding actions.

        Args:
            msg (dict): The message received from the client.

        Returns:
            bool: True if the game should continue, False if the game is over.
        """
        if msg["type"] == "hello":
            self.sendStart()
            print("Game started!")
            return True
        elif msg["type"] == "guess" and msg["word"] not in self.util.words:
            self.guessNotInList()
            print("%s is not in the wordlist." % msg["word"])
            return True
        elif msg["type"] == "guess" and msg["word"] != self.answer:
            markString = self.wrongGuess(msg["word"])
            print(msg["word"][:5] + " is incorrect. Marks: %s" % markString)
            return True
        elif msg["type"] == "guess" and msg["word"] == self.answer:
            self.correctGuess()
            print("Solved in " + str(len(self.guessList)+1) + " guesses! The secret word was %s!" % self.answer[:5])
            return False
            
    def sendStart(self):
            """
            Sends a start message to the server.

            This method sends a JSON-encoded start message to the server
            using the socket connection.

            Parameters:
                None

            Returns:
                None
            """
            startMsg = {"type": "start"}
            self.mysocket.send(json.dumps(startMsg).encode())

    def guessNotInList(self):
        """
        Sends a retry message to the client with the current guess list.

        Returns:
            None
        """
        retryMsg = {"type": "retry", "guesses": self.guessList}
        self.mysocket.send(json.dumps(retryMsg).encode())

    def wrongGuess(self, guess):
        """
        Sends a retry message to the client with the current guess list and returns the marks as a string.

        Parameters:
        guess (str): The word guessed by the player.

        Returns:
        str: The marks as a string.

        """
        marks = self.util.getMarks(guess, self.answer)
        self.guessList.append({"word": guess, "marks": marks})
        retryMsg = {"type": "retry", "guesses": self.guessList}
        self.mysocket.send(json.dumps(retryMsg).encode())
        return "["+str(marks[0])+str(marks[1])+str(marks[2])+str(marks[3])+str(marks[4])+"]"
    
    def correctGuess(self):
        """
        Sends a 'bye' message to the client with the correct answer and the number of guesses made.

        Returns:
            None
        """
        byeMsg = {"type": "bye", "answer": self.answer, "numGuesses": len(self.guessList)+1}
        self.mysocket.send(json.dumps(byeMsg).encode())