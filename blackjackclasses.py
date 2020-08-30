import random
import collections

class Card:
    SPADES = chr(9824)
    HEARTS = chr(9825)
    DIAMONDS = chr(9826)
    CLUBS = chr(9827)

    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value

    def show(self):
        print('{} {}'.format(self.suit, self.name), end=' ')

class Deck:
    def __init__(self):
        self.cards = []
        for suit in (Card.HEARTS, Card.SPADES, Card.CLUBS, Card.DIAMONDS):
            self.cards.append(Card('A', suit, 1))
            for value in range(2, 11):
                self.cards.append(Card(str(value), suit, value))
            self.cards.append(Card('J', suit, 11))
            self.cards.append(Card('Q', suit, 12))
            self.cards.append(Card('K', suit, 13))

    def shuffle(self):
        for i in range(len(self.cards)):
            r = random.randint(0, 51) # inclusive of 51
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self, n=1):
        hand = []
        for _ in range(n):
            if self.isEmpty():
                break
            hand.append(self.cards.pop())
        return hand

    def isEmpty(self):
        return self.cards == []

    def show(self):
        for card in self.cards:
            card.show()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck, n=1):
        self.hand += deck.drawCard(n)

    def showHand(self):
        print('{}'.format(self.name))
        for card in self.hand:
            card.show()

    def showHandbySuit(self):
        print('{}'.format(self.name))
        cards = collections.defaultdict(list)
        for card in self.hand:
            cards[card.suit].append(card.name)
        for suit in cards:
            print('{} : {}'.format(suit, ' '.join(cards[suit])))

    def calPoints(self):
        res = 0
        for card in self.hand:
            res += card.value
        print('Points: {}'.format(res))
        return res

if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    grant = Player('Grant')
    bonnie = Player('Bonnie')
    xiang = Player('Xiang')
    liang = Player('Liang')
    for i in range(2):
        grant.draw(deck)
        bonnie.draw(deck)
        xiang.draw(deck)
        liang.draw(deck)
    for player in (grant, bonnie, xiang, liang):
        player.showHandbySuit()
        player.calPoints()
        print()