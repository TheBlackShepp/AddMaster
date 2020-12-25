import os

from flask import Flask, render_template, request

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
    ) 

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/')
    def index():
        return render_template('login.html')
    
    @app.route('/create-account')
    def createAccount():
        return render_template('create-account.html')
    
    return app