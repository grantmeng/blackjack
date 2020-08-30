import random
import sys
from blackjackclasses import *

#Check if hand is natural 21 or not
def natural(hand):
    a,t = False, False
    for h in hand:
        if "A" in h: a = True
        if "10" in h: t = True
    if a and t: return True
    return False
    
#Calculate total value of hand
def total(hand,b):
    val = 0
    for h in hand:
        if "J" in h or "K" in h or "Q" in h or "10" in h: val += 10 
        elif h[0] == "A": 
            if b == True:
                if val + 11 > 21: val += 1
                else: val += 11
            else:
                val += int(input("What value would you like the Ace to be? "))
        else: val += int(h[0])
    return val
'''
deck = ["2♠️","2♥️","2♢","2♣️","3♠️","3♥️","3♢","3♣️"
        ,"4♠️","4♥️","4♢","4♣️","5♠️","5♥️","5♢","5♣️","6♠️","6♥️","6♢"
        ,"6♣️","7♠️","7♥️","7♢","7♣️","8♠️","8♥️","8♢","8♣️","9♠️","9♥️",
        "9♢","9♣️","10♠️","10♥️","10♢","10♣️","J♠️","J♥️","J♢","J♣️",
        "Q♠️","Q♥️","Q♢","Q♣️","K♠️","K♥️","K♢","K♣️","A♠️","A♥️","A♢","A♣️"]
'''
deck = Deck()
player,dealer = [],[]

#Card distribution
random.shuffle(deck)
for _ in range(2):
    player.append(deck.pop())
    dealer.append(deck.pop())
print("Your cards are",player)
print("One of the dealer's cards is",[str(dealer[0])])

p,d,ptotal,dtotal = "",True,total(player,False),total(dealer,True)

#Determining natural blackjack
if natural(player) and natural(dealer):
    print("You have tied with the dealer!")
    sys.exit()
elif natural(player): 
    print("You have won because of a natural BlackJack!")
    sys.exit()
elif natural(dealer):
    print("You have lost to the dealer because the dealer had a natural BlackJack!")
    sys.exit()

#Hiting or standing
while p != "Stand" or d == True:
    
    print("Would you like to Hit or Stand?")
    
    p = input()
    if p == "Hit": 
        player.append(deck.pop())
        ptotal += total([player[-1]],False) #Adding recent card to total
        print("Your hand is now",player)
        if ptotal > 21: 
            print("Your hand has been busted!")
            sys.exit()
        
    print("Dealer's Turn")

    if dtotal < 17: 
        print("The dealer has chosen to hit.")
        dealer.append(deck.pop())
        dtotal += total([dealer[-1]],True)
        
        if dtotal > 21: 
            print("The dealer's hand has been busted!")
            print("The dealer's cards were",dealer)
            sys.exit()
        
    else: #If dealer's hand >= 17, it has to stand
        d = False 
        print("The dealer has chosen to stand.")
        
print("The dealer's hand is",dealer)

#End results
if ptotal > dtotal: print("You have won!")    
elif ptotal < dtotal: print("You have lost to the dealer!")
else: print("There was a tie!")

    
        
    
        
    

    
    


        
        



