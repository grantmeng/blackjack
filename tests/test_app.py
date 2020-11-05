import json

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'Welcome to Blackjack!' in res.data
