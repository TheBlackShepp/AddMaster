from Back.DatabaseController import DatabaseController
from Back.Enums import TipoCore, TipoUsuario
from Herramientas.SimpleTools import ControlVariables
from datetime import date


database_controller: DatabaseController = DatabaseController()


class CoreBase:
    # region Variables
    _control_variables: ControlVariables = ControlVariables()
    _params: str = "params"
    _permission: str = "permission"
    _resultado: str = "post_result"
    _tipo_de_core: TipoCore

    # endregion
    # region Funciones
    def user_have_permission(self, id_usuario: int) -> bool:
        """
        Nos indica si el usaurio puede acceder al sector de esta clase
        """
        resultado: bool = False
        if self._control_variables.variable_correcta_int(id_usuario) is False:
            resultado = False
        elif self._tipo_de_core == TipoCore.CoreBodega:
            tipo = database_controller.user_permission(id_usuario)
            resultado = tipo == TipoUsuario.Personal or tipo == TipoUsuario.Dolores
        elif self._tipo_de_core == TipoCore.CoreReservas:
            tipo = database_controller.user_permission(id_usuario)
            resultado = tipo == TipoUsuario.Administrativo or tipo == TipoUsuario.Dolores
        elif self._tipo_de_core == TipoCore.Sesion:
            resultado = True
        else:
            resultado = False
        return resultado

    def get_dict_params(self, value: bool) -> dict:
        return {self._params: value}

    def get_dict_permission(self, value: bool) -> dict:
        return {self._permission: value}

    def get_dict_resultado(self, value: bool) -> dict:
        return {self._resultado: value}

    # endregion
    def __init__(self, tipo: TipoCore):
        self._tipo_de_core = tipo


class CoreReservas(CoreBase):
    # region POST
    def comprobar_igresar_datos_producto(self, formulario: dict) -> bool:
        """
        Compruba si los datos del formulario recibido posee o no los dotos necesarios
        """
        li = ["nombre", "cantidad", "precio", "fecha_inicio_venta", "fecha_fin_venta", "etiquetas", "descripcion"]
        return self._control_variables.contains_all_list_in_dict(formulario, li)

    def igresar_datos_producto(self, id_usuario: int, formulario: dict) -> dict:
        """
        Ingresa los datos de un producto al core Reservas
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        result: dict = {}
        if self.comprobar_igresar_datos_producto(formulario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                database_controller.igresar_datos_producto(formulario)
                result.update(self.get_dict_resultado(True))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result

    def modificar_datos_producto(self, id_usuario: int, id_producto: int, formulario: dict) -> dict:
        """
        Modifica los datos de un producto al core Reservas
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        result: dict = {}
        if self.comprobar_igresar_datos_producto(formulario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update(self.get_dict_resultado(
                    database_controller.modificar_datos_producto(id_producto, formulario)))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result

    def comprobar_dar_alta_cliente(self, formulario: dict) -> bool:
        """
        Compruba si los datos del formulario recibido posee o no los dotos necesarios
        """
        li = ["email", "nombre", "apellido", "apellido2", "telefono", "edad", "fecha_nacimiento", "domicilio", "sexo"]
        return self._control_variables.contains_all_list_in_dict(formulario, li)

    def dar_alta_cliente(self, id_usuario: int, formulario: dict) -> dict:
        """
        Añade un nuevo cliente a la lista
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        result: dict = {}
        if self.comprobar_dar_alta_cliente(formulario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                if formulario.get("pedidos") is None:
                    formulario.update({"pedidos": []})
                print(formulario)
                database_controller.dar_alta_cliente(formulario)
                result.update(self.get_dict_resultado(True))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result

    def dar_baja_cliente(self, id_usuario: int, id_cliente: int) -> dict:
        """
        Da de baja a un cliente
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se ha eliminado el cliente con exito
            post_result False: No se ha eliminado el cliente, ya que probablemente no exista
        """
        result: dict = {}
        if self._control_variables.variable_correcta_list_int([id_usuario, id_cliente]):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update(self.get_dict_params(database_controller.dar_baja_cliente(id_cliente)))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result

    # endregion
    # region GET
    def get_datos_producto(self, id_usuario: int, id_producto: int) -> dict:
        """
        Obtiene los datos de un producto en un diccionario
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        result: dict = {}
        if self._control_variables.variable_correcta_list_int([id_usuario, id_producto]):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_datos_producto(id_producto)
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result

    # endregion
    def __init__(self):
        super().__init__(TipoCore.CoreReservas)


class CoreBodega(CoreBase):
    # region POST

    # endregion
    # region GET

    # endregion
    def __init__(self):
        super().__init__(TipoCore.CoreBodega)


class CoreSeesion(CoreBase):
    def __init__(self):
        super().__init__(TipoCore.Sesion)

    def comprobar_inicio_sesion(self, formulario: dict) -> bool:
        """
        Compruba si los datos del formulario recibido posee o no los dotos necesarios
        """
        li = ["email", "password"]
        return self._control_variables.contains_all_list_in_dict(formulario, li)

    def iniciar_sesion(self, formulario: dict) -> str:
        """
        Inicia sesion
        Devuelve el id del usuario
        Devuelve -1 si no existe
        """
        result: str = ""
        if formulario["email"] == "pato@gmail.com" and formulario["password"] == "PatoPassword1":
            result = "0"
        return result


c = CoreReservas()
"""print(c.get_datos_producto(0, 0))
print(c.modificar_datos_producto(0, 0, {
    "nombre": "Producto 1 modificado",
    "cantidad": 999,
    "precio": 1,
    "fecha_inicio_venta": date.today().__str__(),
    "fecha_fin_venta": date.today().__str__(),
    "etiquetas": ["Etiqueta 1", "Etiqueta 2", "Etiqueta 3"],
    "descripcion": "No hay mucho que poner en un producto ficticio"
}))"""
print(c.dar_alta_cliente(0, {
    "email": "emailtest",
    "nombre": "Pato",
    "apellido": "Willyx",
    "apellido2": "Mixta",
    "telefono": "666666666",
    "edad": 2,
    "fecha_nacimiento": date.today().__str__(),
    "domicilio": "Noooo!",
    "sexo": "M"
}))
database_controller.save_all()





"""from requests import get, post


r = post(url="http://127.0.0.1:8080/igresar_datos_producto", data={"patata": "1", "p": "2"})
if r.status_code == 200:
    print(r.text)"""
"""r = get(url="http://127.0.0.1:8080")
if r.status_code == 200:
    print(r.text)"""
