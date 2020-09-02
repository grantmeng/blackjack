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
connections = []

def threaded_client(conn, curPlayer):
    # send message to the player.
    conn.send(str.encode('Welcome to Blackjack! Please input your name:'))
    while True:
        try:
            player_msg = conn.recv(2048).decode()
            if not player_msg:
                print("No message from player, remove it")
                if conn in connections: connections.remove(conn)
            elif player_msg == 'Hit':
                player = players[curPlayer]
                player.draw(deck)
                hand = player.getHand()
                print('{} got new card, current hand: {}'.format(player.name, hand))
                conn.send(str.encode('Your current hand: {}\n'.format(hand)))
            elif player_msg == 'Stand':
                pass
            else: # player input name
                player = Player(player_msg)
                player.draw(deck, 2)
                players.append(player)
                hand = player.getHand()
                print('{} joined and got two cards: {}'.format(player_msg, hand))
                conn.send(str.encode('Your current hand: {}\n'.format(hand)))
                conn.send(str.encode('Hit or Stand: '))
        except: continue

    # close the connection with the player
    # conn.close()
    # if conn in connections: connections.remove(conn)

curPlayer = 0
while True:
    # establish connection with client.
    conn, addr = s.accept()
    print("{} is connected".format(addr[0]))
    connections.append(conn)
    start_new_thread(threaded_client, (conn, curPlayer))
    curPlayer += 1
#conn.close()
#s.close()