# Mitch Brotherson
# CS1400 - CO1
# Assignment 7

import random
from modules.card import Card

class Deck:
    def __init__(self):
        self.shuffle()

    def shuffle(self):
        self.__deck = []
        for i in range(52):
            self.__deck.append(Card(i))
        random.shuffle(self.__deck)

    def draw(self):
        return self.__deck.pop()

