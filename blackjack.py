import random
import sys
from blackjackclasses import *

deck = Deck()
deck.shuffle()
dealer, player1 = Player('Grant'), Player('Xiang')

#Card distribution
for _ in range(2):
    dealer.draw(deck)
    player1.draw(deck)
for player in (dealer, player1):
    player.showHand()
    player.getPoints()
    print()    

if dealer.getPoints() == float('inf'):
    print("The dealer has won with a natural BlackJack!")
    exit(0)

if player1.getPoints() == float('inf'):
    print("Player has won with a natural BlackJack!")
    exit(0)

p, d = "Hit", True
while p != "Stand" and d:

    print("Would you like to Hit or Stand?")
    
    p = input()
    if p == "Hit": 
        player1.draw(deck)
        print("Your hand is now:")
        player1.showHand()
        if player1.getPoints() == float('-inf'): 
            print("Your hand has been busted!")
            exit(0)
        
    print("Dealer's Turn")

    if dealer.getPoints() < 17: 
        print("The dealer has chosen to hit.")
        dealer.draw(deck)
        dealer.showHand()
        if dealer.getPoints() == float('-inf'): 
            print("The dealer has been busted!")
            exit(0)   
    else: #If dealer's hand >= 17, it has to stand
        d = False
        print("The dealer has chosen to stand.")
        
print("The dealer's hand is:")
dealer.showHand()
print("Your hand is:")
player1.showHand()

#End results
if player1.getPoints() > dealer.getPoints(): print("You have won!")    
elif player1.getPoints() < dealer.getPoints(): print("You have lost to the dealer!")
else: print("There was a tie!")