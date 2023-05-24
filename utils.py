import os, sys
from random import randint
class Utils:
    wordlist = open(os.path.join(sys.path[0], "wordlist.txt"))
    words = wordlist.readlines()
    for word in words:
        word = word[:5]

    #get a random word in the available words
    def getRandWord(self):
        #number of words in the list
        numWords = len(self.words)
        #random word in the list of words
        randNum = randint(1, numWords)
        randWord = self.words[randNum - 1]
        return randWord