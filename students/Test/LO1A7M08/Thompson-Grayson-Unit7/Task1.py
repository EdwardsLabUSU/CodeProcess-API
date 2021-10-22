# Grayson Thompson
# CS 1400 LO!
# Assignment 7 - task 1


import time
from deck import Deck


def main():
    players = []
    while True:
        numPlayers = int(input("How many players are dealing in?(1-5) "))
        if 0 < numPlayers <= 5:
            for x in range(numPlayers + 1):
                players.append([])
            break
        else:
            continue

    playerBank = []
    for x in range(len(players) - 1):
        playerBank.append(100)

    betMoneys = []
    
    hitHold = "\n 1) hit"
    hitHold += "\n 2) hold\n"

    play = True
    while play:

        while True:
            deck = Deck()
            for x in range(len(players) - 1):
                if playerBank[x] <= 0:
                    print("\nplayer " + str(x + 1) + " lost")
                else:
                    print("\n" + "Player " + str(x + 1) + "\n" + "Cash to Bet: $" + str(playerBank[x]))
                    betMoney = input("Place a bet Amount (min $5): ")
                    if playerBank[x] < 5:
                        betMoney = playerBank[x]
                    elif not betMoney.isdigit() or not playerBank[x] >= int(betMoney) >= 5:
                        print("\ninvalid input")
                        while True:
                            betMoney = input("Enter a bet (min $5): ")
                            if betMoney.isdigit() and playerBank[x] >= int(betMoney) >= 5:
                                break

                    print("bet:  $" + str(betMoney))
                    betMoneys.append(betMoney)
                   
            break

        for x in range(2):
            for y in range(len(players)):
                players[y].append(deck.draw())
        
        playerTotals = []
        
        for x in range(len(players) - 1):
            if playerBank[x] <= 0:
                continue

            else:
                print("\nDealers Hand")
                print(players[len(players) - 1][1])
                print()
                
                print("player " + str(x + 1))
                print(players[x][0])
                print(players[x][1])
                print(hitHold)

                while True:
                    choice = input("")
                    if choice == "1":
                        players[x].append(deck.draw())
                        for y in players[x]:
                            print(y)

                        total = 0
                       
                        for card in players[x]:
                            if "Ace" in str(card):
                                total += 11
                            elif str(card.getNickName()).isalpha():
                                total += 10
                            else:
                                total += card.getCardValue()

                        if total > 21:
                            ace = 0
                            for y in players[x]:
                                if "Ace" in str(y):
                                    ace += 1
                                    total += 1
                            total -= ace * 11
                        print("\t" + str(total))

                        if total > 21:
                            message = "BUST!"
                            print(message)
                            playerTotals.append(0)
                            break

                        continue

                    elif choice == "2":
                        total = 0
                        for card in players[x]:
                            if "Ace" in str(card):
                                total += 11
                            elif str(card.getNickName()).isalpha():
                                total += 10
                            else:
                                total += card.getCardValue()

                        if total > 21:
                            ace = 0
                            for y in players[x]:
                                if "Ace" in str(y):
                                    ace += 1
                                    total += 1
                            total -= ace * 11
                        print("\t" + str(total))

                        playerTotals.append(total)
                        break
                    else:
                        print("Invalid")
                        continue

        print("\nDealers Hand")
        print()
        print(players[-1][0])
        print(players[-1][1])
        
        dealerHand = 0
        
        for card in players[-1]:
            if "Ace" in str(card):
                dealerHand += 11
            elif str(card.getNickName()).isalpha():
                dealerHand += 10
            else:
                dealerHand += card.getCardValue()
        if dealerHand > 21:
            dealerHand = 12

        while dealerHand < 17:
            print()
            time.sleep(1)
            print()
            print("Dealer takes a card")
            players[-1].append(deck.draw())
            time.sleep(1)
            print(players[-1][-1])

            dealerHand= 0
            for card in players[-1]:
                if "Ace" in str(card):
                    dealerHand += 11
                elif str(card.getNickName()).isalpha():
                    dealerHand += 10
                else:
                    dealerHand += card.getCardValue()
            if dealerHand > 21:
                ace = 0
                for y in players[-1]:
                    if "Ace" in str(y):
                        ace += 1
                        dealerHand += 1
                dealerHand -= ace * 11
            if dealerHand > 21:
                message = "BUST!"
                print(message)
                dealerCard = 1
                break
            if 17 < dealerHand < 21:
                print()
                time.sleep(1)
                print("The Dealer Holds")
                continue
        time.sleep(1)
        print()
        if dealerHand == 1:
            pass
        else:
            print("Dealer total")
            print(dealerHand)
        print()

        for x in range(len(players) - 1):
            if playerBank[x] <= 0:
                pass
            elif playerTotals[x] < dealerHand:
                print("player " + str(x + 1) + " lost", end=", ")
                playerBank[x] -= int(betMoneys[x])
                print("Total: ", playerBank[x])

            elif playerTotals[x] > dealerHand:
                print("player " + str(x + 1) + " won", end=",  ")
                playerBank[x] += int(betMoneys[x])
                print("Total: ", playerBank[x])

            else:
                print("player " + str(x + 1) + " tied", end=", ")
                print("Total: ", playerBank[x])

        print()

        noMoney = 0
        for money in playerBank:
            if money == 0:
                noMoney += 1
        if noMoney == len(playerBank):
            again = "n"

        else:
            again = input("Want To Play Again? (Yes, No) ")

        if again == "yes":
            for hand in players:
                hand.clear()
            betMoneys.clear()
            continue

        else:
            print()
            print("Thanks for playing The Game Of Blackjack!")

            sort = True
            while sort:
                sort = False

                for x in range(len(playerBank) - 1):
                    if playerBank[x] > playerBank[x + 1]:
                        playerBank[x], playerBank[x + 1] = playerBank[x + 1], playerBank[x]
                        sort = True

            print()
          
            for x in range(len(playerBank) - 1, -1, -1):
                print("player " + str(x + 1) + " $" + str(playerBank[x]))
                print()

            play = False


main()