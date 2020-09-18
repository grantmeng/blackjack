from config import *
from blackjackclasses import *
from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

deck = Deck()
deck.shuffle()
players = {'Dealer': Player('Dealer')}
for _ in range(2): players['Dealer'].draw(deck)

@app.route('/')
def index():
    return render_template('join.html')

@app.route('/join', methods=['POST'])
def join():
    username = request.form['username']
    if username in players:
        return render_template('join.html', err_msg='%s already exists.' % username)
    player = Player(username)
    for _ in range(2): player.draw(deck)
    players[username] = player
    return render_template('blackjack.html', players=players, player=player)

if __name__ == '__main__':
   app.run(SERVER, PORT, DEBUG)