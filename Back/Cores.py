from Enums import TipoCore
from Herramientas.SimpleTools import ControlVariables
from datetime import date


class CoreBase:
    # region Variables
    _control_variables: ControlVariables = ControlVariables()
    _params: str = "params"
    _permission: str = "permission"
    __resultado: str = "post_result"
    _tipo_de_core: TipoCore

    # endregion
    # region Funciones
    def user_have_permission(self, id_usuario: str) -> bool:
        """
        Nos indica si el usaurio puede acceder al sector de esta clase
        """
        resultado: bool = False
        if self._control_variables.variable_correcta(id_usuario) is False:
            resultado = False
        elif self._tipo_de_core == TipoCore.CoreBodega:
            if id_usuario == "002":
                resultado = True
        elif self._tipo_de_core == TipoCore.CoreReservas:
            if id_usuario == "001":
                resultado = True
        elif self._tipo_de_core == TipoCore.Sesion:
            resultado = True
        else:
            resultado = False
        return resultado

    def get_dict_params(self, value: bool) -> dict:
        return {self._params: value}

    def get_dict_permission(self, value: bool) -> dict:
        return {self._permission: value}

    # endregion
    def __init__(self, tipo: TipoCore):
        self._tipo_de_core = tipo


class CoreReservas(CoreBase):
    def __init__(self):
        super().__init__(TipoCore.CoreReservas)

    def comprobar_igresar_datos_producto(self, formulario: dict) -> bool:
        """
        Compruba si los datos del formulario recibido posee o no los dotos necesarios
        """
        li = ["nombre", "cantidad", "precio", "fecha_inicio_venta", "fecha_fin_venta", "etiquetas", "descripcion"]
        return self._control_variables.contains_all_list_in_dict(formulario, li)

    def get_datos_producto(self, id_usuario: str, id_producto: str) -> dict:
        """
        Obtiene los datos de un producto en un diccionario
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        result: dict = {}
        if self._control_variables.variable_correcta_list([id_usuario, id_producto]):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update({
                    self._permission: True,
                    "nombre": "Producto 1",
                    "cantidad": 100,
                    "precio": 1000,
                    "fecha_inicio_venta": date.today(),
                    "fecha_fin_venta": date.today(),
                    "etiquetas": ["Etiqueta 1", "Etiqueta 2", "Etiqueta 3"],
                    "descripcion": "No hay mucho que poner en un producto ficticio"
                })
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result


class CoreBodega(CoreBase):
    def __init__(self):
        super().__init__(TipoCore.CoreBodega)


class CoreSeesion(CoreBase):
    def __init__(self):
        super().__init__(TipoCore.Sesion)

    def comprobar_inicio_sesion(self, formulario: dict):
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


d = {
    "nombre": "",
    "cantidad": "",
    "precio": "",
    "fecha_inicio_venta": "",
    "fecha_fin_venta": "",
    "etiquetas": "",
    "descripcion": ""
}

c = CoreReservas()
print(c.get_datos_producto("", "001"))
print(c.get_datos_producto("001", ""))
print(c.get_datos_producto("002", "001"))
print(c.get_datos_producto("001", "001"))
print(c.comprobar_igresar_datos_producto(d))





"""from requests import get, post


r = post(url="http://127.0.0.1:8080/igresar_datos_producto", data={"patata": "1", "p": "2"})
if r.status_code == 200:
    print(r.text)"""
"""r = get(url="http://127.0.0.1:8080")
if r.status_code == 200:
    print(r.text)"""
