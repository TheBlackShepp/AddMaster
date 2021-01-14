from flask import Flask, render_template, request, jsonify, redirect, make_response, abort, send_from_directory
from ControladorCookies import ControladorCookies
from Back.Cores import CoreSeesion, CoreReservas, CoreBodega
from Herramientas.SimpleTools import ControlVariables
from Back.Enums import TipoUsuario, TipoMateria
from fpdf import FPDF
from os import path

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
# region Otras funciones
def easy_function(cookie_jar, lambda_func, param=None) -> any:
    resultado = None
    cookiesesion = controlador_cookies.get_cookie_by_cookie_jar(cookie_jar)
    # Si no tiene cookie
    if cookiesesion is None:
        abort(404, "Cookie not found")
    # Si tiene cookie pero no es valida
    elif controlador_cookies.contiene_cookie(cookiesesion) is False:
        abort(404, "Cookie not valid")
    # Si tiene cookie y es valida
    else:
        id_usuario = controlador_cookies.get_id(cookiesesion)
        if param is not None:
            resultado = lambda_func(id_usuario, param)
        else:
            resultado = lambda_func(id_usuario)
    return resultado


def string_to_pdf(id_usuario: int, formulario: dict) -> str:
    result: str = ""
    pedido = core_reservas.get_datos_pedido(id_usuario, formulario)
    if pedido['params'] is True and pedido["permission"] is True:
        result = f'Pedido numero {pedido["id"]}.pdf'
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Courier', 'B', 16)
        pdf.cell(40, 10, pedido.__str__(), fill=1)
        pdf.output(result, 'F')
    return result


# endregion
# region Paginas
@app.route('/index', methods=["GET"])
def index_i():
    return redirect("/")


@app.route('/', methods=["GET"])
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
        return redirect("/")
    # Si tiene cookie pero no es valida
    elif controlador_cookies.contiene_cookie(cookiesesion) is False:
        return redirect("/")
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
        formulario = request.form.to_dict(flat=False)
        # Si los parametros recibidos son correctos
        if sesion_control.comprobar_inicio_sesion(formulario):
            id_usuario: int = sesion_control.iniciar_sesion(formulario)
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


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        cookiesesion = controlador_cookies.get_cookie_by_cookie_jar(request.cookies)
        if controlador_cookies.contiene_cookie(cookiesesion) is True:
            controlador_cookies.eliminar_cookie(cookiesesion)
            return indexhtml("", True)
        else:
            return redirect("/")
    else:
        return redirect("/")


# endregion
# region Posts
# region Producto
@app.route("/igresar_datos_producto", methods=["POST"])
def igresar_datos_producto():
    return easy_function(request.cookies, core_reservas.igresar_datos_producto, request.form.to_dict(flat=False))


@app.route("/modificar_datos_producto", methods=["POST"])
def modificar_datos_producto():
    return easy_function(request.cookies, core_reservas.modificar_datos_producto, request.form.to_dict(flat=False))


@app.route("/get_datos_producto", methods=["POST"])
def get_datos_producto():
    return easy_function(request.cookies, core_reservas.get_datos_producto, request.form.to_dict(flat=False))


@app.route("/get_lista_productos", methods=["POST"])
def get_lista_productos():
    return easy_function(request.cookies, core_reservas.get_lista_productos)


# endregion
# region Clientes
@app.route("/dar_alta_cliente", methods=["POST"])
def dar_alta_cliente():
    return easy_function(request.cookies, core_reservas.dar_alta_cliente, request.form.to_dict(flat=False))


@app.route("/dar_baja_cliente", methods=["POST"])
def dar_baja_cliente():
    return easy_function(request.cookies, core_reservas.dar_baja_cliente, request.form.to_dict(flat=False))


@app.route("/modificar_datos_cliente", methods=["POST"])
def modificar_datos_cliente():
    return easy_function(request.cookies, core_reservas.modificar_datos_cliente, request.form.to_dict(flat=False))


@app.route("/get_datos_cliente", methods=["POST"])
def get_datos_cliente():
    return easy_function(request.cookies, core_reservas.get_datos_cliente, request.form.to_dict(flat=False))


@app.route("/get_lista_clientes", methods=["POST"])
def get_lista_clientes():
    return easy_function(request.cookies, core_reservas.get_lista_clientes)


# endregion
# region Pedido
@app.route("/igresar_datos_pedido", methods=["POST"])
def igresar_datos_pedido():
    return easy_function(request.cookies, core_reservas.igresar_datos_pedido, request.form.to_dict(flat=False))


@app.route("/eliminar_pedido", methods=["POST"])
def eliminar_pedido():
    return easy_function(request.cookies, core_reservas.eliminar_pedido, request.form.to_dict(flat=False))


@app.route("/modificar_datos_pedido", methods=["POST"])
def modificar_datos_pedido():
    return easy_function(request.cookies, core_reservas.modificar_datos_pedido, request.form.to_dict(flat=False))


@app.route("/get_datos_pedido", methods=["POST"])
def get_datos_pedido():
    return easy_function(request.cookies, core_reservas.get_datos_pedido, request.form.to_dict(flat=False))


@app.route("/get_lista_pedidos", methods=["POST"])
def get_lista_pedidos():
    return easy_function(request.cookies, core_reservas.get_lista_pedidos)


# endregion
# region Usuarios
@app.route("/ingresar_usuario", methods=["POST"])
def ingresar_usuario():
    return easy_function(request.cookies, core_bodega.ingresar_usuario, request.form.to_dict(flat=False))


@app.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    return easy_function(request.cookies, core_bodega.eliminar_usuario, request.form.to_dict(flat=False))


@app.route("/modificar_usuario", methods=["POST"])
def modificar_usuario():
    return easy_function(request.cookies, core_bodega.modificar_usuario, request.form.to_dict(flat=False))


@app.route("/get_datos_usuario", methods=["POST"])
def get_datos_usuario():
    return easy_function(request.cookies, core_bodega.get_datos_usuario, request.form.to_dict(flat=False))


@app.route("/get_lista_usuarios", methods=["POST"])
def get_lista_usuarios():
    return easy_function(request.cookies, core_bodega.get_lista_usuarios)


# endregion
# region Materia Prima
@app.route("/igresar_datos_materia_prima", methods=["POST"])
def igresar_datos_materia_prima():
    return easy_function(request.cookies, core_bodega.igresar_datos_materia_prima, request.form.to_dict(flat=False))


@app.route("/eliminar_meteria_prima", methods=["POST"])
def eliminar_meteria_prima():
    return easy_function(request.cookies, core_bodega.eliminar_meteria_prima, request.form.to_dict(flat=False))


@app.route("/get_datos_materia_prima", methods=["POST"])
def get_datos_materia_prima():
    return easy_function(request.cookies, core_bodega.get_datos_materia_prima, request.form.to_dict(flat=False))


@app.route("/get_lista_materias_primas", methods=["POST"])
def get_lista_materias_primas():
    return easy_function(request.cookies, core_bodega.get_lista_materias_primas)


# endregion
# endregion
@app.route("/imprimir", methods=["POST"])
def imprimir():
    return {"pdfname": easy_function(request.cookies, string_to_pdf, request.form.to_dict(flat=False))}


@app.route("/get_materia_prima_name/<int:id>")
def get_materia_prima_name(id):
    if id < 0:
        return "No existe"
    elif id > TipoMateria.Alvarinio.value:
        return "No existe"
    else:
        v: TipoMateria = TipoMateria(id)
        return v.__str__()


@app.route('/getFile/<string:filename>', methods=['GET'])
def download(filename: str):
    if path.exists(filename):
        return send_from_directory(directory=".", filename=filename)
    else:
        abort(404, "Fila not faund")


if __name__ == '__main__':
    app.run(
        port=8080,
        host='0.0.0.0',
        debug=False)  # , ssl_context='adhoc')
