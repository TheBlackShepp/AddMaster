import string
import random
from flask import Blueprint, render_template, jsonify, request, redirect, url_for

listIdsRandom = []

login = Blueprint('login', __name__, template_folder='./templates')

# permisos
# 0 -> permiso todo
# 1 -> administrador
# 2 -> personal
listUser= [('camilo@gmail.com','camiloUs', 'abc123', 1), ('dolores@gmail.com', 'dolores', 'abc123', 0), ('jose@gmail.com', 'jose', 'abc123', 2)]

@login.route('/doLogin', methods=['POST'])
def doLogin():
    # user= request.form['username']
    # passw= request.form['password']
    
    return render_template('index.html')
    
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

