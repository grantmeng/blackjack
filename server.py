from config import *
from blackjackclasses import *
import socket
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((SERVER, PORT))
except socket.error as e: print(e)

s.listen(MAX_PLAYERS)
print("Waiting for player to join")

deck = Deck(); deck.shuffle()
players = [None] * MAX_PLAYERS
connections = [None] * MAX_PLAYERS

def threaded_client(conn, curPlayer):
    # send message to the player and ask player to input name
    while True: 
        conn.send(str.encode('Player {}: welcome to Blackjack! Please input your name.'.format(curPlayer)))
        player_msg = conn.recv(2048).decode()
        if not player_msg: continue
        players[curPlayer] = Player(player_msg)
        break
    
    # the player created, initially assign two cards
    player = players[curPlayer]
    player.draw(deck, 2)
    hand = player.getHand()
    print('Player {}: {} joined and got two cards: {}'.format(curPlayer, player_msg, hand))
    points = player.getPoints()
    if points == float('inf'):
        print('Player {}: {} won with blackjack!: {}'.format(curPlayer, player.name, hand))
        conn.send(str.encode('Player {}: you won with blackjack!: {}\n'.format(curPlayer, hand)))
    else:
        conn.send(str.encode('Player {}: your current hand: {}\n'.format(curPlayer, hand)))
        conn.send(str.encode('Player {}: Hit or Stand?'.format(curPlayer)))

    # continue the game       
    while True:
        try:
            player_msg = conn.recv(2048).decode()
            if player_msg == 'Hit':
                player.draw(deck)
                hand = player.getHand()
                print('Player {}: {} got new card, current hand: {}'.format(curPlayer, player.name, hand))
                points = player.getPoints()
                if points == float('-inf'):
                    print('Player {}: {} bursted with hand: {}'.format(curPlayer, player.name, hand))
                    conn.send(str.encode('Player {}, you bursted with hand: {}\n'.format(curPlayer, hand)))
                else:
                    conn.send(str.encode('Player {}, your current hand: {}\n'.format(curPlayer, hand)))
            elif player_msg == 'Stand':
                conn.send(str.encode('Player {}, your current hand: {}\n'.format(curPlayer, hand)))
            else:
                pass
        except: continue

    # close the connection with the player
    # conn.close()
    # if conn in connections: connections.remove(conn)

curPlayer = 0
while True:
    # establish connection with client.
    conn, addr = s.accept()
    print("{} is connected".format(addr[0]))
    connections[curPlayer] = conn
    start_new_thread(threaded_client, (conn, curPlayer))
    curPlayer += 1
#conn.close()
#s.close()