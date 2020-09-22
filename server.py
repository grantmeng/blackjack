from config import *
from CardGame import *
from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

deck = Deck(); deck.shuffle()
players = {}; playerIPs = {}
startgame = False

@app.route('/')
def index():
    return render_template('join.html')

@app.route('/join', methods=['POST'])
def join():
    username = request.form['username']
    ip = request.remote_addr
    if username in players:
        if ip != players[username].ip:
            return render_template('join.html', err_msg='Player %s already exists, use another name.' % username)
        else:
            return render_template('lobby.html', players=players, player=players[username])
    player = Player(username); player.ip = ip
    for _ in range(2): player.draw(deck)
    players[username] = player
    return render_template('lobby.html', players=players, player=player)

@app.route('/start', methods=['POST'])
def start():
    username = request.form['username']
    return render_template('lobby.html', players=players, player=players[username], startgame=True)



if __name__ == '__main__':
    app.run(SERVER, PORT, DEBUG)