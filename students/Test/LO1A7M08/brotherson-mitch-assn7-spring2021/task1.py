# Mitch Brotherson
# CS1400 - CO1
# Assignment 7

from modules.card import Card
from modules.deck import Deck

deck = Deck()

def playerBets(wallets):
    print(wallets)
    for i in range(len(wallets)):
        print(i + 1, wallets[i])
        if wallets[i][0] < 5 and wallets[i][0] > 0:
            wallets[i][1] = wallets[i][0] 
            wallets[i][0] = 0
        elif wallets[i][0] ==  0:
            print("skipped player" + str(i)) 
        else:
            bet = eval(input("Please input bet amount (at least $5): "))
            if wallets[i][0] >= bet:
                wallets[i][0] -= bet
                wallets[i][1] += bet
            else:
                eval(input("sorry you don't have that much, enter an amount you have: "))
         
         
def cardDeal(table):
    deck = Deck()
    deck.shuffle()
    for i in range(len(table)):
        table[i].append(deck.draw())
    for i in range(len(table)):
        table[i].append(deck.draw())
    dealerCard = table[-1][-1]
    print("The dealers card is: " + str(dealerCard))
    

def playerHand(player):
    for i in range(len(player)):
        print(player[i])
        
        
def sumOfCardValues(player):
    sum = 0
    for j in range(len(player)):
        cardValues = player[j].getCardValue()
        if cardValues == 1:
            sum += 11
        elif cardValues > 10:
            sum += 10
        else:
            sum += cardValues
    print(sum)


def hitHold(player):
    for i in range(len(player)):
        if sumOfCardValues() <= 21:
            userInput = input("Do you want to hit or hold? ")
            if userInput == "hit" or userInput == "Hit" or userInput == "HIT":
                player[i].append(deck.draw)
        

def main():
    numPlayer = eval(input("Please enter number of players (1 - 5): "))
    table = []
    wallets = []
    for i in range(numPlayer + 1):
        table.append([])
    # last list is dealer
    
    for i in range(numPlayer):
        wallets.append([100, 0])
        
    playerBets(wallets)
    
    cardDeal(table)
    
    for i in range(numPlayer):
        print("player " + str(i + 1) + "'s cards are ")
        playerHand(table[i])
        sumOfCardValues(table[i])
        hitHold(table[i])
                    
#test
   
main()