from config import *
from CardGame import *
from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
app = Flask(__name__)
app.secret_key = 'blackjack' # has to be set to use session, which is a client side session
#app.config.from_object(__name__)
#server_session = Session()
#server_session.init_app(app)

deck = Deck(); deck.shuffle()
players = {}
start_game = False

@app.route('/')
def index():
    session['cur_user'] = None # initialize curren user name
    session['start_game'] = False # initialize game status
    return render_template('join.html')

@app.route('/join', methods=['POST'])
def join():
    if session['cur_user']: # current user already logged in
        return render_template('lobby.html', cur_user=session['cur_user'], players=players, start_game=start_game)
    session['cur_user'] = request.form['username']
    ip = request.remote_addr
    if session['cur_user'] in players:
        if ip != players[session['cur_user']].ip:
            return render_template('join.html', err_msg='Player %s already exists, use another name.' % session['cur_user'])
        else:
            return render_template('lobby.html', cur_user=session['cur_user'], players=players, start_game=start_game)
    # create a new player
    if len(players) >= MAX_PLAYERS:
        return render_template('join.html', err_msg='Already reached maximum %s players.' % MAX_PLAYERS)
    player = Player(session['cur_user']); player.ip = ip
    for _ in range(2): player.draw(deck)
    players[session['cur_user']] = player
    return render_template('lobby.html', cur_user=session['cur_user'], players=players, start_game=start_game)

@app.route('/start', methods=['POST'])
def start():
    start_game = True
    #return redirect(url_for('join'))
    return render_template('lobby.html', cur_user=session['cur_user'], players=players, start_game=start_game)

if __name__ == '__main__':
    app.run(SERVER, PORT, DEBUG)