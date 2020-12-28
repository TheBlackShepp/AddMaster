import os
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect, CSRFError
from markupsafe import escape

from login import login

# CSRF token
csrf = CSRFProtect()


app = Flask(__name__)
app.register_blueprint(login)

app.config.from_mapping(
    SECRET_KEY='addMaster'
)
csrf.init_app(app)

@app.route('/')
def loginPage():
    return render_template('login.html')

@app.route('/dashboard')
def index():
    return render_template('index.html', permission=2)

@app.route('/dashboard/<path:subpath>')
def dashboardSubPath(subpath):
    print(f'Sub path -> {escape(subpath)}')
    return render_template('index.html', page=f'{subpath}', permission=2)

@app.route('/create-account')
def createAccount():
    return render_template('create-account.html')
    
@app.errorhandler(404)
def page_not_found(e):
    """Page not found."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(
        debug=True, use_debugger=True, use_reloader=True,
        host='0.0.0.0',
        port=8080)  # This line is required to run Flask on repl.it