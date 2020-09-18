from config import *
from blackjackclasses import *
from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

deck = Deck()
deck.shuffle()
dealer = Player('Dealer')
for _ in range(2): dealer.draw(deck)

@app.route('/')
def index():
    return render_template('join.html')

@app.route('/join', methods=['POST'])
def join():
    username = request.form['username']
    player = Player(username)
    for _ in range(2): player.draw(deck)
    return render_template('blackjack.html', player=player, dealer=dealer)

if __name__ == '__main__':
   app.run(SERVER, PORT, DEBUG)