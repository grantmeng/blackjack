from CardGame import *
import collections

def test_card():
    card = Card('A', Card.SPADES, 1)
    assert card.name == 'A'
    assert card.suit == '\u2660'
    assert card.value == 1

def test_deck():
    deck = Deck()
    suits = collections.defaultdict(list)
    for card in deck.cards:
        suits[card.suit].append(card.value) 
    assert sorted(suits[Card.SPADES]) == list(range(1, 14))
    assert sorted(suits[Card.HEARTS]) == list(range(1, 14))
    assert sorted(suits[Card.CLUBS]) == list(range(1, 14))
    assert sorted(suits[Card.DIAMONDS]) == list(range(1, 14))

def test_player():
    user = Player('Grant')
    assert user.name == 'Grant'
    assert isinstance(user.rule, Blackjack)
    assert not user.hand
