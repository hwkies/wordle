import json
import sys
sys.path.append('..')
from utils import Utils

class Client:
    """
    Represents a client for the Wordle game.

    Attributes:
    - util: An instance of the Utils class.
    """

    util = Utils()

    def yellowLetters(self, word, marks, guessedWord):      
        """
        Checks if a given word contains a yellow letter.

        Parameters:
        - word: The word to check.
        - marks: A list of numerical marks.
        - guessedWord: The guessed word.

        Returns:
        - True if the word contains a yellow letter, False otherwise.
        """
        yellows = []
        for idx in range(5):
            if marks[idx] == 1:
                yellows.append(guessedWord[idx])
        for letter in yellows:
            if letter not in word:
                return False
        return True

    def shrinkWordlist(self, marks, guessedWord):
        """
        Shrinks the wordlist according to a set of numerical marks and a guessed word.

        Parameters:
        - marks: A list of numerical marks.
        - guessedWord: The guessed word.
        """
        newWords = []
        for word in self.util.words:
            for i in range(5):
                if guessedWord[i] == word[i] and marks[i] == 0:
                    newWords.append(word)
                    break
                elif guessedWord[i] != word[i] and marks[i] == 2:
                    newWords.append(word) 
                    break
                elif guessedWord[i] == word[i] and marks[i] == 1:
                    newWords.append(word)
                    break
                elif self.yellowLetters(word, marks, guessedWord) == False:
                    newWords.append(word)   
                    break  
        for line in newWords:
            self.util.words.remove(line)

    def dataHandler(self, client, hostname, port):
        """
        Creates a client server connection and sends a hello message to the server.

        Parameters:
        - client: The client object.
        - hostname: The hostname of the server.
        - port: The port number of the server.
        """
        client.connect((hostname, port))
        hello = json.dumps({'type': 'hello'}) + '\n'
        client.send(hello.encode())
        response = client.recv(25600)
        response = response.decode()
        stringResp = json.loads(response)
        self.responseHandler(stringResp, client)

    def responseHandler(self, response, client):
        """
        Handles server responses and returns the final flag.

        Parameters:
        - response: The server response.
        - client: The client object.

        Returns:
        - The final flag.
        """
        stringResp = response
        if stringResp["type"] == "start":
            guess = json.dumps({'type': 'guess', 'word': self.util.getRandWord()}) + '\n'
            print(guess)
            client.send(guess.encode())
            stringResp = json.loads(client.recv(25600).decode())
            print(stringResp)
        while stringResp["type"] == "retry":
            lastGuess = stringResp["guesses"][len(stringResp["guesses"]) - 1]
            self.shrinkWordlist(lastGuess["marks"], lastGuess["word"])
            guess = json.dumps({'type': 'guess', 'word': self.util.getRandWord()}) + '\n'
            print(guess)
            client.send(guess.encode())
            stringResp = json.loads(client.recv(25600).decode())
            print(stringResp)
        
        print("You took %d guesses!" % stringResp["numGuesses"])
        print("The secret word was: %s!" % stringResp["answer"][:5])
        return


#take in an array of integers representing green, yellow, or black letters
#choose next available possible word from wordlist
#proj1.3700.network kiesman.h