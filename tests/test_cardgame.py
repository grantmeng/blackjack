from CardGame import *

def test_player():
    user = Player('Grant')
    assert user.name == 'Grant'
    assert isinstance(user.rule, Blackjack)
    assert not user.hand
