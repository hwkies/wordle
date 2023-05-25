import json
import sys
sys.path.append('..')
import utils

class Server:
    mysocket = None
    util = utils.Utils()
    answer = util.getRandWord()
    guessList = []

    def __init__(self, sock):
        self.mysocket = sock

    def typeParser(self, msg):
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
        startMsg = {"type": "start"}
        self.mysocket.send(json.dumps(startMsg).encode())

    def guessNotInList(self):
        retryMsg = {"type": "retry", "guesses": self.guessList}
        self.mysocket.send(json.dumps(retryMsg).encode())

    def wrongGuess(self, guess):
        marks = self.util.getMarks(guess, self.answer)
        self.guessList.append({"word": guess, "marks": marks})
        retryMsg = {"type": "retry", "guesses": self.guessList}
        self.mysocket.send(json.dumps(retryMsg).encode())
        return "["+str(marks[0])+str(marks[1])+str(marks[2])+str(marks[3])+str(marks[4])+"]"
    
    def correctGuess(self):
        byeMsg = {"type": "bye", "answer": self.answer, "numGuesses": len(self.guessList)+1}
        self.mysocket.send(json.dumps(byeMsg).encode())