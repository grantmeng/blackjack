from config import *
from blackjackclasses import *
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('static', filename='login.html'))

@app.route('/login', methods=['POST'])
def login():
    user = request.form['name']
    return redirect(url_for('success', name=user))

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

if __name__ == '__main__':
   app.run(SERVER, PORT, DEBUG)