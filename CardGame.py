import random
import collections
from Rules import *

class Card:
    SPADES = '\u2660'
    HEARTS = '\u2665'
    DIAMONDS = '\u2666'
    CLUBS = '\u2663'

    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.suit_name = 'clubs'
        if suit == Card.SPADES: self.suit_name = 'spades'
        elif suit == Card.HEARTS: self.suit_name = 'hearts'
        elif suit == Card.DIAMONDS: self.suit_name = 'diamonds'
        self.value = value

    def show(self):
        print('{} {}'.format(self.suit, self.name), end=' ')

    def get(self):
        return '{} {}'.format(self.suit, self.name)

class Deck:
    def __init__(self):
        self.cards, self.done = [], []
        for suit in (Card.HEARTS, Card.SPADES, Card.CLUBS, Card.DIAMONDS):
            self.cards.append(Card('A', suit, 1))
            self.cards.append(Card('J', suit, 11))
            self.cards.append(Card('Q', suit, 12))
            self.cards.append(Card('K', suit, 13))
            for value in range(2, 11):
                self.cards.append(Card(str(value), suit, value))

    def shuffle(self):
        self.cards += self.done
        self.done = []
        for i in range(len(self.cards)):
            r = random.randint(0, 51) # inclusive of 51
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self, n=1):
        hand = []
        for _ in range(n):
            if self.isEmpty(): break
            card = self.cards.pop()
            hand.append(card)
            self.done.append(card)
        return hand

    def isEmpty(self):
        return self.cards == []

    def show(self):
        for card in self.cards: card.show()

class Player:
    def __init__(self, name, rule=Blackjack):
        self.name = name
        self.rule = rule()
        self.hand = []

    def draw(self, deck, n=1):
        new_hand = deck.drawCard(n)
        self.hand += new_hand
        return new_hand

    def getHand(self):
        return self.hand

    def resetHand(self):
        self.hand = []
    
    def showHand(self):
        cards = []
        for card in self.hand:
            cards.append('{}{}'.format(card.suit, card.name))
        return ','.join(cards)

    def showFirstCard(self):
        if self.hand:
            return '{}{}'.format(self.hand[0].suit, self.hand[0].name)
        return ''

    def getHandbySuit(self):
        cards = collections.defaultdict(list)
        for card in self.hand:
            cards[card.suit].append(card.name)
        return cards

    def showHandBySuit(self):
        cards = collections.defaultdict(list)
        for card in self.hand:
            cards[card.suit].append(card.name)
        hand = ''
        for suit in cards:
            hand += '{}:{}; '.format(suit, ','.join(cards[suit]))
        return hand

    def points(self):
        return self.rule.getPoints(self.hand)
        

if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    grant = Player('Grant')
    bonnie = Player('Bonnie')
    xiang = Player('Xiang')
    liang = Player('Liang')
    for _ in range(3):
        grant.draw(deck)
        bonnie.draw(deck)
        xiang.draw(deck)
        liang.draw(deck)
    for player in (grant, bonnie, xiang, liang):
        print('{}: {}'.format(player.name, player.showHand()))
        print('{}: {}'.format(player.name, player.showHandBySuit()))
        print(player.points())