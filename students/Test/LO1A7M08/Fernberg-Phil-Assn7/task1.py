# Phil Fernberg
# CS 1400 - L01
# Assignment 7 - Task 1

import time
from card import Card
from deck import Deck

def main():
    
    print("Welcome to Pseudo-Blackjack!\n\n")
    
    # Determine number of players
    players = []
    numPlayers = eval(input("How many players? "))
    for i in range(numPlayers):
        players.append("Player " + str(i + 1))
        

    # Start and manage account balances
    acctBalances = []
    startBal = 100
    for i in range(numPlayers):
        acctBalances.append(startBal)
    
    # Display balances and get bets
    print("\nACCOUNT BALANCES")
    for i in players:
        print(i + ": " + str(startBal))
    
    bets = []
    for i in range(numPlayers):
        bets.append(eval(input("\nBet for " + players[i] + ": ")))
        
    # Deal the cards    
    numHands = numPlayers + 1
    numWithDealer = numHands
    
    
    
    
    # Play a round
    inPlay = True
    while inPlay:
        hands = []
        for i in range(numHands):
            hands.append([])
        deck = deal(hands)
        playRound(players, hands, deck)
    
        print("\nThe Dealer's hand is: ") # Reveal Dealer's hand
        print(str(hands[len(hands) - 1][0]))
        print(str(hands[len(hands) - 1][1]))
        
        print()
        seeWinner(players, hands, bets, acctBalances) # Determine winner
        print()
        
        playChoice = input("Play again (Y/N)?").upper()
        if playChoice == "N":
            inPlay = False
        else:
            print("\nHere we go again...\n")
            
        
    # Goodbye
    print("Thanks for playing!!")
    acctBalList = [(i, acctBalances[i]) for i in range(len(players))]
    acctBalList = sorted(acctBalList, key=lambda x: x[1], reverse=True)
    #sort account balances and display
    print("Final Scores:")
    for pair in acctBalList:
        print(f"\t{players[pair[0]]} : ${pair[1]}")
    
def deal(hands):
    cardCnt = 2
    deck = Deck()
    for i in range(len(hands)):
        for j in range(cardCnt):
            hands[i].append(deck.draw())
    # Display dealer hand second card
    print("\nThe Dealer's first card is " + str(hands[len(hands) - 1][1]))
    return deck

def playRound(playerList, handList, deck):
    for i in range(len(playerList)): 
        play = True
        while play:
            print("\n" + str(playerList[i]) + " Hand:")
            for j in range(len(handList[i])):
                print(str(handList[i][j]))
            playerScore = 0
            for j in handList[i]:
                playerScore += j.getCardValue()
            if playerScore > 21:
                print("BUST!")
                break
            else:
                choice = (eval(input("\n1) Hit \n2) Hold \nWhat do you want to do?")))
                if choice == 2:
                    play = False
                else:
                    handList[i].append(deck.draw())
    
    
def seeWinner(playerList, handList, betList, balanceList):
    dealScore = 0
    for i in handList[len(handList) - 1]:
        dealScore += i.getCardValue()
    for i in range(len(playerList)):
        playerScore = 0
        for j in handList[i]:
            playerScore += j.getCardValue()
        if playerScore > 21:
            res = "Loses"
        elif playerScore > dealScore or dealScore > 21:
            res = "Wins"
        elif playerScore == dealScore:
            res = "Ties"
        else:
            res = "Loses"
            
        print(playerList[i] + " " + res)
        
    payouts(playerList, res, betList, balanceList) 
        
def payouts(playerList, result, betList, balanceList):
    for i in range(len(balanceList)):
        if result == "Wins":
            balanceList[i] += betList[i]
            print(playerList[i], "New Account Balance:", balanceList[i])
        elif result == "Ties":
            balanceList[i] += 0
            print(playerList[i], "New Account Balance:", balanceList[i])
        elif result == "Loses":
            balanceList[i] -= betList[i]
            print(playerList[i], "New Account Balance:", balanceList[i])
        else:
            balanceList[i] -= betList[i]
            print(playerList[i], "New Account Balance:", balanceList[i])


main()