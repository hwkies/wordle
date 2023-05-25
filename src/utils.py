import os
import sys
import random

class Utils:
    wordlist = open(os.path.join(sys.path[len(sys.path)-1], "wordlist.txt"))
    words = wordlist.readlines()
    for word in words:
        word = word[:5]

    #get a random word in the available words
    def getRandWord(self):
        #number of words in the list
        numWords = len(self.words)
        #random word in the list of words
        randNum = random.randint(1, numWords)
        randWord = self.words[randNum - 1]
        return randWord
    
    def getMarks(self, word, answer):
        marks = [0, 0, 0, 0, 0]
        for idx in range(5):
            if word[idx] == answer[idx]:
                marks[idx] = 2
            elif word[idx] != answer[idx] and word[idx] in answer:
                marks[idx] = 1
        return marks