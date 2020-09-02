from config import *
from blackjackclasses import *
import socket
import sys

# create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVER, PORT))
except socket.error as e: print(e)

while True:
    try:
        server_msg = client.recv(2048).decode()
        print(server_msg)
        player_msg = None
        while not player_msg: player_msg = input()
        client.send(str.encode(player_msg))
    except socket.error as e: print(e)