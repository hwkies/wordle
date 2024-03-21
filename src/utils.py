import os
import sys
import random

class Utils:
    """
    Utility class for wordle game.
    """

    wordlist = open(os.path.join(sys.path[len(sys.path)-1], "wordlist.txt"))
    words = list(map(lambda word: word[:5], wordlist.readlines()))

    def getRandWord(self):
        """
        Get a random word from the available words.

        Returns:
            str: Random word.
        """
        numWords = len(self.words)
        randNum = random.randint(1, numWords)
        randWord = self.words[randNum - 1]
        return randWord
    
    def getMarks(self, word, answer):
        """
        Get the marks by comparing the answer to the secret word.

        Args:
            word (str): Secret word.
            answer (str): User's answer.

        Returns:
            list: List of marks indicating correct and partially correct positions.
        """
        marks = [0, 0, 0, 0, 0]
        for idx in range(5):
            if word[idx] == answer[idx]:
                marks[idx] = 2
            elif word[idx] != answer[idx] and word[idx] in answer:
                marks[idx] = 1
        return marks