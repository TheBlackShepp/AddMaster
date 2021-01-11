from flask import Flask, render_template, request, jsonify, redirect, make_response, abort
from ControladorCookies import ControladorCookies
from Back.Cores import CoreSeesion, CoreReservas, CoreBodega
from Herramientas.SimpleTools import ControlVariables
from Back.Enums import TipoUsuario

# Instancias
app = Flask(__name__)
control_variables = ControlVariables()
controlador_cookies = ControladorCookies()
sesion_control = CoreSeesion()
core_reservas = CoreReservas()
core_bodega = CoreBodega()


# region PaginasWebFunctions
def prepararHTML(url: str, cookie: str, expire: bool, tipo: TipoUsuario = TipoUsuario.NULL) -> any:
    # Le enviamos el index
    resp = make_response(render_template(url, permission=tipo.value))
    if control_variables.variable_correcta(cookie):
        # Le enviamos la cookie de sesion
        if expire:
            resp.set_cookie(controlador_cookies.cookie_value(), str(cookie), httponly=True, expires=0)
        else:
            resp.set_cookie(controlador_cookies.cookie_value(), str(cookie), httponly=True)
    return resp


def indexhtml(cookie: str, expire: bool) -> any:
    return prepararHTML("index.html", cookie, expire)


def homehtml(cookie, expire: bool, tipo: TipoUsuario) -> any:
    return prepararHTML("home.html", cookie, expire, tipo)


# endregion
@app.route('/', methods=["GET"])
def index_i():
    return redirect("/index")


@app.route('/index', methods=["GET"])
def index():
    resultado = None
    cookiesesion = controlador_cookies.get_cookie_by_cookie_jar(request.cookies)
    # Si no tiene cookie
    if cookiesesion is None:
        resultado = indexhtml("", False)
    # Si tiene cookie pero no es valida
    elif controlador_cookies.contiene_cookie(cookiesesion) is False:
        resultado = indexhtml("", True)
    # Si tiene cookie y es valida
    else:
        id_usuario = controlador_cookies.get_id(cookiesesion)
        resultado = homehtml(None, False, sesion_control.get_tipo_usuario(id_usuario))
    return resultado

@app.route('/index/<path:subpath>', methods=["GET"])
def dashboardSubPath(subpath):
    resultado = None
    cookiesesion = controlador_cookies.get_cookie_by_cookie_jar(request.cookies)
    # Si no tiene cookie
    if cookiesesion is None:
        resultado = indexhtml("", False)
    # Si tiene cookie pero no es valida
    elif controlador_cookies.contiene_cookie(cookiesesion) is False:
        resultado = indexhtml("", True)
    # Si tiene cookie y es valida
    else:
        id_usuario = controlador_cookies.get_id(cookiesesion)
        resultado = homehtml(None, False, sesion_control.get_tipo_usuario(id_usuario))
    return resultado


@app.route('/login', methods=["GET", "POST"])
def login():
    resultado = None
    # Si es la peticion de POST de inicio de sesion
    if request.method == "POST":
        # Si los parametros recibidos son correctos
        if sesion_control.comprobar_inicio_sesion(request.form):
            id_usuario: int = sesion_control.iniciar_sesion(request.form)
            # Si las credenciales son correctas
            if control_variables.variable_correcta_int(id_usuario):
                # Generamos un cookie
                cookie = controlador_cookies.generar_cookie(id_usuario)
                resultado = homehtml(cookie, False, sesion_control.get_tipo_usuario(id_usuario))
            # Si las credenciales no son correctas, lo reenviamos al login
            else:
                resultado = indexhtml("", False)
        # Si los parametros recibidos no son correctos
        else:
            abort(400, "No se han recibido los parametros correctamente")
    # Si la peticion es de tipo GET le redireccionamos a login
    # Donde se comprobara si tiene cookie de sesion o no
    elif request.method == "GET":
        resultado = redirect("/")
    return resultado


@app.route("/igresar_datos_producto", methods=["POST"])
def igresar_datos_producto():




    print(type(request.form))
    return "http://0.0.0.0:8080"


if __name__ == '__main__':
    app.run(
        port=8080,
        host='0.0.0.0',
        debug=True)  # , ssl_context='adhoc')
