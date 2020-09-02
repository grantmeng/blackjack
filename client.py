from config import *
from blackjackclasses import *
import socket
import sys

# create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVER, PORT))
    #print(pickle.loads(client.recv(2048)))
except socket.error as e: print(e)

print('Welcome to Blackjack, please input your name:')
name = input()
try:
    client.send(str.encode(name))
    response = client.recv(2048).decode()
    print(response)
    client.send(str.encode(response))
except socket.error as e: print(e)