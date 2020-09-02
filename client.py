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
        name = input()
        client.send(str.encode(name))
    except socket.error as e: print(e)