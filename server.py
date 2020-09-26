import random
from config import *
from CardGame import *
from flask import Flask, request, render_template, url_for, session, current_app
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'blackjack' # has to be set to use session, which is a client side session
# initialize application wide variables, which are shared among all users/requests
with app.app_context():
    current_app.deck = Deck(); current_app.deck.shuffle()
    current_app.players = {}
    current_app.players_order = []
    current_app.start_game = False
    current_app.cur_order = 0
socketio = SocketIO(app, logger=True)

@app.route('/')
def index():
    session['me'] = None # initialize curren user name, this is client session
    return render_template('join.html')

@app.route('/join', methods=['POST', 'GET'])
def join():
    if session['me']: # current user already logged in
        return render_template('lobby.html', 
            me=session['me'], 
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
                me=username, 
                players=current_app.players, 
                players_order=current_app.players_order,
                cur_order=current_app.cur_order,
                start_game=current_app.start_game)
    # create a new player
    if len(current_app.players) >= MAX_PLAYERS:
        return render_template('join.html', err_msg='Already reached maximum %s players.' % MAX_PLAYERS)
    session['me'] = username # set current user session
    player = Player(username); player.ip = ip
    for _ in range(2): player.draw(current_app.deck)
    current_app.players[username] = player
    current_app.players_order.append(username)
    return render_template('lobby.html', 
        me=username, 
        players=current_app.players, 
        players_order=current_app.players_order,
        cur_order=current_app.cur_order,
        start_game=current_app.start_game)

@socketio.on('start')
def start(data):
    current_app.start_game = True
    random.shuffle(current_app.players_order)
    socketio.emit('server done', {'msg': 'done'})

@socketio.on('hit')
def hit(data):
    player = current_app.players[session['me']]
    if player.points() == float("-inf") or player.points() == float("inf") \
        or player.points() == 21: # busted or blackjack or 21 points, pass to next player
        if current_app.cur_order == len(current_app.players_order) - 1:
            current_app.cur_order = 0
        else:
            current_app.cur_order += 1
    else: # get new card
        player.draw(current_app.deck)
    socketio.emit('server done', {'msg': 'done'})
    
@socketio.on('stand')   
def stand(data):
    if current_app.cur_order == len(current_app.players_order) - 1:
        current_app.cur_order = 0
    else:
        current_app.cur_order += 1
    socketio.emit('server done', {'msg': 'done'})

if __name__ == '__main__':
    #app.run(SERVER, PORT, DEBUG)
    socketio.run(app, host=SERVER, port=PORT, debug=True)