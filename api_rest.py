from flask import Flask, render_template, request, jsonify, redirect, make_response, abort
from ControladorCookies import ControladorCookies


# Instancias
app = Flask(__name__)
controlador_cookies = ControladorCookies()


@app.route("/igresar_datos_producto", methods=["POST"])
def igresar_datos_producto():
    print(type(request.form))
    return "http://0.0.0.0:8080"


@app.route("/", methods=["GET"])
def index():
    return "http://0.0.0.0:8080"


if __name__ == '__main__':
    app.run(
        port=8080,
        host='0.0.0.0',
        debug=False)  # , ssl_context='adhoc')
