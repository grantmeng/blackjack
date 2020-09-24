import random
from config import *
from CardGame import *
from flask import Flask, request, render_template, redirect, url_for, session, current_app

app = Flask(__name__)
app.secret_key = 'blackjack' # has to be set to use session, which is a client side session
# initialize application wide variables, which are shared among all users/requests
with app.app_context():
    current_app.deck = Deck(); current_app.deck.shuffle()
    current_app.players = {}
    current_app.players_order = []
    current_app.start_game = False
    current_app.cur_order = 0

@app.route('/')
def index():
    session['cur_user'] = None # initialize curren user name, this is client session
    return render_template('join.html')

@app.route('/join', methods=['POST'])
def join():
    if session['cur_user']: # current user already logged in
        return render_template('lobby.html', 
            cur_user=session['cur_user'], 
            players=current_app.players, 
            players_order=current_app.players_order,
            cur_order=current_app.cur_order,
            start_game=current_app.start_game)
    username = request.form['username']
    ip = request.remote_addr
    if username in current_app.players:
        if ip != current_app.players[username].ip: # new user with duplicate name
            return render_template('join.html', err_msg='Player %s already exists, use another name.' % username)
        else: # same user logged in
            return render_template('lobby.html', 
                cur_user=username, 
                players=current_app.players, 
                players_order=current_app.players_order,
                cur_order=current_app.cur_order,
                start_game=current_app.start_game)
    # create a new player
    if len(current_app.players) >= MAX_PLAYERS:
        return render_template('join.html', err_msg='Already reached maximum %s players.' % MAX_PLAYERS)
    session['cur_user'] = username # set current user session
    player = Player(username); player.ip = ip
    for _ in range(2): player.draw(current_app.deck)
    current_app.players[username] = player
    current_app.players_order.append(username)
    return render_template('lobby.html', 
        cur_user=username, 
        players=current_app.players, 
        players_order=current_app.players_order,
        cur_order=current_app.cur_order,
        start_game=current_app.start_game)

@app.route('/start', methods=['POST'])
def start():
    if not current_app.start_game:
        current_app.start_game = True
        random.shuffle(current_app.players_order)
    return render_template('lobby.html', 
        cur_user=session['cur_user'], 
        players=current_app.players, 
        players_order=current_app.players_order,
        cur_order=current_app.cur_order,
        start_game=True)

@app.route('/restart', methods=['POST'])
def restart():
    current_app.deck.shuffle()
    current_app.start_game = False
    random.shuffle(current_app.players_order)
    return render_template('lobby.html', 
        cur_user=session['cur_user'], 
        players=current_app.players, 
        players_order=current_app.players_order,
        cur_order=current_app.cur_order,
        start_game=False)

@app.route('/hit', methods=['POST'])
def hit():
    player = current_app.players[session['cur_user']]
    for _ in range(1): player.draw(current_app.deck)
    if player.points() == float("-inf"):
        if current_app.cur_order == len(current_app.players_order) - 1:
            current_app.cur_order = 0
        else:
            current_app.cur_order += 1
    return render_template('lobby.html', 
        cur_user=session['cur_user'], 
        players=current_app.players, 
        players_order=current_app.players_order,
        cur_order=current_app.cur_order,
        start_game=current_app.start_game)

@app.route('/stand', methods=['POST'])
def stand():
    # order only changes if it's current user
    if current_app.players_order[current_app.cur_order] == session['cur_user']:
        if current_app.cur_order == len(current_app.players_order) - 1:
            current_app.cur_order = 0
        else:
            current_app.cur_order += 1
    return render_template('lobby.html', 
        cur_user=session['cur_user'], 
        players=current_app.players, 
        players_order=current_app.players_order,
        cur_order=current_app.cur_order,
        start_game=current_app.start_game)

if __name__ == '__main__':
    app.run(SERVER, PORT, DEBUG)