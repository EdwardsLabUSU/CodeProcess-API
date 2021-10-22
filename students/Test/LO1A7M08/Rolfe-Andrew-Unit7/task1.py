# Andrew Rolfe
# CS1400 - 001
# Assignment task1 - unit6
from deck import Deck
import time

def main():
    hands = []# hands[0] is always dealer hand
    playerInfo = []
    numPlayers = 6
    
    while numPlayers > 5:
        numPlayers = eval(input("How many players? (1-5)"))
        if numPlayers > 5:
            print("Please enter a number 1-5")
            continue
        for i in range(numPlayers + 1):
            msg = "Player " + str(i)
            hands.append([])
            if i > 0:
                playerInfo.append([msg, 100, 0, hands[i], False])
        
    deck = Deck()
    playAgain = True
    while playAgain:
        for i in playerInfo:
            i[2] = 0
            i[3].clear()
            i[4] = False
        hands[0].clear()
            
        for i in playerInfo:
            bet = eval(input(i[0] + " how much would you like to bet? (must be greater than $5) $"))
            if bet < 5:
                if i[1] - 5 > 0:
                    i[2] = 5
                    print("Your bet has been set to $5")
                else:
                    i[2] = i[3]
                    print("Your balance was less than 5 and you have gone all in")
            elif bet > i[1]:
                print("You do not have that much money, you have been set to go all in at $" + str(i[1]))
                i[2] = i[1]
            else:
                i[2] = bet
            
        for i in range(2):
            for j in hands:
                j.append(deck.draw())
                
        for i in playerInfo:
            
            hold = False
            print("\n********** " +i[0] + "'s turn ***********\n")
            
            while not hold:
                
                sum = getSum(i[3])
                
                print(i[3])
                    
                print("Your total is: " + str(sum))
                if sum > 21:
                    print("You have busted\n")
                    time.sleep(1)
                    i[4] = True
                    break
                
                hit = eval(input("Would you like to \n1) hit \n2) hold \n"))
                if hit == 2:
                    hold = True
                    print()
                    time.sleep(1)
                else:
                    card = deck.draw()
                    print("You drew a " + str(card))
                    i[3].append(card)
                    
        print("Dealers cards are: ")               
        print(hands[0][0])
        print(hands[0][1])
        dealerSum = getSum(hands[0])
        print("Total:" + str(dealerSum))
        time.sleep(3)
        if dealerSum > 21:
            print("The dealer busts")
        elif dealerSum > 21:
            print("The dealer holds")
        while dealerSum < 17:
            
            time.sleep(2)
            card = deck.draw()
            hands[0].append(card)
            print("The dealer hits and draws a " + str(card))
            dealerSum = getSum(hands[0])
            print("Total: " + str(dealerSum))
            if dealerSum > 21:
                print("The dealer busts")
            elif dealerSum >= 17:
                print("The dealer holds")
                
        print("\nTIME TO DISPLAY WHO IS GOOD AT BLACK JACK\n")
        
        time.sleep(1)
        for i in range(len(playerInfo)):
            sum = getSum(playerInfo[i][3])
            time.sleep(2)
            if playerInfo[i][4]:
                playerInfo[i][1] -= playerInfo[i][2]
                print(playerInfo[i][0] + " busted and has a new balance of $" + str(playerInfo[i][1]))
                continue
            elif dealerSum > 21:
                playerInfo[i][1] += playerInfo[i][2]
                print(playerInfo[i][0] + " won and has a new balance of $" + str(playerInfo[i][1]))
                continue
            elif sum < dealerSum:
                playerInfo[i][1] -= playerInfo[i][2]
                print(playerInfo[i][0] + " lost and has a new balance of $" + str(playerInfo[i][1]))
            elif sum == dealerSum:
                print(playerInfo[i][0] + " tied and has a balance of $" + str(playerInfo[i][1]))
            elif sum > dealerSum:
                playerInfo[i][1] += playerInfo[i][2]
                print(playerInfo[i][0] + " won and has a new balance of $" + str(playerInfo[i][1]))
                    
        again = eval(input("Would you like to play again? \n1) yes\n2) no\n"))
        if again == 1:
            count = 0
            for i in range(len(playerInfo) - 1):
                if playerInfo[i][1] <= 0:
                    hands.remove(playerInfo[i][3])
                    playerInfo.remove(playerInfo[i])
                    count += 1
        elif again == 2:
            playAgain = False
    print("Thanks for playing")
        
        
def getSum(list):
    sum = 0
    ace = False
    for i in range(len(list)):
        add = list[i].getCardValue()
        if add == 1:
            ace = True
            add = 11
        elif add > 10:
            add = 10
        sum += add
    if sum > 21 and ace:
        sum - 10
    return sum
        

main()
