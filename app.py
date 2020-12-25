import os

from flask import Flask, render_template, request


app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY='dev',
) 

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/create-account')
def createAccount():
    return render_template('create-account.html')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080)  # This line is required to run Flask on repl.it

    
