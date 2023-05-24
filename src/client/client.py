import json
import sys
sys.path.append('..')
from utils import Utils

class Client:
    util = Utils()

    #return true if a given word contains a yellow letter, false otherwise
    def yellowLetters(self, word, marks, guessedWord):      
        yellows = []
        for idx in range(5):
            if marks[idx] == 1:
                yellows.append(guessedWord[idx])
        for letter in yellows:
            if letter not in word:
                return False
            return True

    #shrink the wordlist according to a set of numerical marks and a guessed word
    def shrinkWordlist(self, marks, guessedWord):
        newWords = []
        for word in self.util.words:
            for i in range(5):
                #letter in guess is black and in the same spot in dictionary word
                if guessedWord[i] == word[i] and marks[i] == 0:
                    newWords.append(word)
                    break
                #letter in guess is green and not in same spot in dictionary word
                elif guessedWord[i] != word[i] and marks[i] == 2:
                    newWords.append(word) 
                    break
                #letter in guess is yellow and in same spot in dictionary word
                elif guessedWord[i] == word[i] and marks[i] == 1:
                    newWords.append(word)
                    break
                #dictionary word does not contain a yellow letter
                elif self.yellowLetters(word, marks, guessedWord) == False:
                    newWords.append(word)   
                    break  
        #remove all words that need to be removed from wordlist                 
        for line in newWords:
            self.util.words.remove(line)

    #create a client server connection and send a hello message to server
    def dataHandler(self, client, hostname, port):
        client.connect((hostname, port))
        #send data to the server
        hello = json.dumps({'type': 'hello'}) + '\n'
        client.send(hello.encode())
        #what is the server response?
        response = client.recv(25600)
        response = response.decode()
        #un-jsonify server response
        stringResp = json.loads(response)
        self.responseHandler(stringResp, client)

    #handle server responses and return the final flag
    def responseHandler(self, response, client):
        stringResp = response
        #if start message, get id and make a guess
        if stringResp["type"] == "start":
            guess = json.dumps({'type': 'guess', 'word': self.util.getRandWord()}) + '\n'
            print(guess)
            client.send(guess.encode())
            stringResp = json.loads(client.recv(25600).decode())
            print(stringResp)
        #while guess is incorrect, make new guess    
        while stringResp["type"] == "retry":
            #edit wordlist and try new word
            lastGuess = stringResp["guesses"][len(stringResp["guesses"]) - 1]
            self.shrinkWordlist(lastGuess["marks"], lastGuess["word"])
            guess = json.dumps({'type': 'guess', 'word': self.util.getRandWord()}) + '\n'
            print(guess)
            client.send(guess.encode())
            stringResp = json.loads(client.recv(25600).decode())
            print(stringResp)
        #print the final flag
        
        print("You took %d guesses!" % stringResp["numGuesses"])
        print("The secret word was: %s!" % stringResp["answer"][:5])
        return


#take in an array of integers representing green, yellow, or black letters
#choose next available possible word from wordlist
#proj1.3700.network kiesman.h