import uuid
from Herramientas.SimpleTools import ControlVariables


class ControladorCookies:
    # region Variables
    __cookies_dict: dict = {}  # Diccionario de los usuarios actualmente logeados
    __cookieValue: str = "sescontrol"
    __control_variables: ControlVariables

    # endregion
    # region Cookies
    def __get_cookie_por_usuario(self, id_persona: int) -> str:
        """
        Devuelve la cookie asociada a un id
        Si no se encuentra nada devuelve un string vacio
        """
        result: str = ""
        for key, value in self.__cookies_dict.items():
            if id_persona == value:
                result = key
                break
        return result

    def contiene_cookie(self, cookie: str) -> bool:
        """
        Nos dice si una cookie esta contenida o no (True o False)
        """
        return self.__cookies_dict.__contains__(cookie)

    def generar_cookie(self, id_persona: int) -> str:
        """
        Genera una cookie para un id recibido
        Si el id ya estaba en la lista devuelve la misma cookie
        """
        cookie: str = self.__get_cookie_por_usuario(id_persona)
        if self.__control_variables.variable_correcta(cookie) is False:
            cookie = str(uuid.uuid4())
            self.__cookies_dict[cookie] = id_persona
        return cookie

    def eliminar_cookie(self, cookie: str) -> bool:
        """
        Elimina una cookie
        Si no la encuentra devuelve False
        """
        result: bool = False
        if self.__cookies_dict.__contains__(cookie) is True:
            del self.__cookies_dict[cookie]
            result = True
        return result

    def get_id(self, cookie: str) -> int:
        """
        Devuelve un el id del usuario que contiene la cookie
        Si la cookie no esta asociada a ningun usuario devuelve -1
        """
        result = self.__cookies_dict.get(cookie)
        if result is None:
            result = -1
        return result

    def cookie_value(self) -> str:
        """
        Devuelve la clave(key) que se añade al inicio de toda cookie en los clientes:
            key=cookie_generada_por_uuid
        """
        return self.__cookieValue

    def get_cookie_by_cookie_jar(self, cookie_jar: dict) -> str:
        resultado = cookie_jar.get(self.__cookieValue)
        if resultado is None:
            resultado = ""
        return resultado

    # endregion
    def __init__(self):
        self.__cookies_dict = {}
        self.__control_variables = ControlVariables()
