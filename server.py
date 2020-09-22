from config import *
from CardGame import *
from flask import Flask, request, render_template, redirect, url_for, session, current_app
app = Flask(__name__)
app.secret_key = 'blackjack' # has to be set to use session, which is a client side session

deck = Deck(); deck.shuffle()
players = {}

# initialize game status, this is application wide variable/data, shared among all other users/requests
with app.app_context():
    current_app.start_game = False

@app.route('/')
def index():
    session['cur_user'] = None # initialize curren user name, this is client session
    return render_template('join.html')

@app.route('/join', methods=['POST'])
def join():
    if session['cur_user']: # current user already logged in
        return render_template('lobby.html', cur_user=session['cur_user'], players=players, start_game=current_app.start_game)
    username = request.form['username']
    ip = request.remote_addr
    if username in players:
        if ip != players[username].ip: # new user with duplicate name
            return render_template('join.html', err_msg='Player %s already exists, use another name.' % username)
        else: # same user logged in
            return render_template('lobby.html', cur_user=username, players=players, start_game=current_app.start_game)
    # create a new player
    if len(players) >= MAX_PLAYERS:
        return render_template('join.html', err_msg='Already reached maximum %s players.' % MAX_PLAYERS)
    session['cur_user'] = username # set current user session
    player = Player(username); player.ip = ip
    for _ in range(2): player.draw(deck)
    players[username] = player
    return render_template('lobby.html', cur_user=username, players=players, start_game=current_app.start_game)

@app.route('/start', methods=['POST'])
def start():
    current_app.start_game = True
    return render_template('lobby.html', cur_user=session['cur_user'], players=players, start_game=True)
    #return redirect(url_for('join'))

if __name__ == '__main__':
    app.run(SERVER, PORT, DEBUG)