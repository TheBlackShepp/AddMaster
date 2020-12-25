import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def index():
    return render_template('index.html')

@app.route('/create-account')
def createAccount():
    return render_template('create-account.html')
    

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080)  # This line is required to run Flask on repl.it