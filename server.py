from config import *
from blackjackclasses import *
import socket
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((SERVER, PORT))
except socket.error as e: print(e)

s.listen(4)
print("Waiting for player to join")

deck = Deck(); deck.shuffle()
players = []

def threaded_client(conn):
    # send message to the player.
    # conn.send(players[player])
    response = ""
    while True:
        try:
            name = conn.recv(2048).decode()
            if not name:
                print("No player name")
                break
            player = Player(name)
            players.append(player)
            player.draw(deck, 2)
            cards = player.showHand()
            print('Player {} joined and got two cards:'.format(name))
            conn.send('Hi')
            player_response = conn.recv(2048).decode()
            print(players)
        except: break

    # close the connection with the player
    # conn.close()

while True:
    # establish connection with client.
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))