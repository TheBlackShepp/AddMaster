from Enums import TipoUsuario
from datetime import date

class IDClass:
    # region Variables
    __id: int

    # endregion
    # region Operadores
    def __init__(self, id: int = -1):
        self.__id = id

    # endregion
    # region Getters
    @property
    def id(self) -> int:
        return self.__id

    # endregion
    # region Setters
    @id.setter
    def id(self, value: int):
        self.__id = value

    # endregion


class Persona(IDClass):
    # region Variables
    __email: str
    __nombre: str
    __apellido: str
    __apellido2: str
    __telefono: str
    __edad: int
    __fecha_nacimiento: date
    __domicilio: str
    __sexo: str

    # endregion
    # region Operadores
    def __init__(self, email: str = "", nombre: str = "", apellido: str = "", apellido2: str = "", telefono: str = "",
                 edad: int = 0, fecha_nacimiento: date = None, domicilio: str = "", sexo: str = "", id: int = -1):
        super().__init__(id=id)
        self.__email = email
        self.__nombre = nombre
        self.__apellido = apellido
        self.__apellido2 = apellido2
        self.__telefono = telefono
        self.__edad = edad
        self.__fecha_nacimiento = fecha_nacimiento
        self.__domicilio = domicilio
        self.__sexo = sexo

    # endregion
    # region Getters
    @property
    def email(self) -> str:
        return self.__email

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def apellido(self) -> str:
        return self.__apellido

    @property
    def apellido2(self) -> str:
        return self.__apellido2

    @property
    def telefono(self) -> str:
        return self.__telefono

    @property
    def edad(self) -> int:
        return self.__edad

    @property
    def fecha_nacimiento(self) -> date:
        return self.__fecha_nacimiento

    @property
    def domicilio(self) -> str:
        return self.__domicilio

    @property
    def sexo(self) -> str:
        return self.__sexo
    # endregion
    # region Setters
    @email.setter
    def email(self, value: str):
        self.__email = value

    @nombre.setter
    def nombre(self, value: str):
        self.__nombre = value

    @apellido.setter
    def apellido(self, value: str):
        self.__apellido = value

    @apellido2.setter
    def apellido2(self, value: str):
        self.__apellido2 = value

    @telefono.setter
    def telefono(self, value: str):
        self.__telefono = value

    @edad.setter
    def edad(self, value: int):
        self.__edad = value

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, value: date):
        self.__fecha_nacimiento = value

    @domicilio.setter
    def domicilio(self, value: str):
        self.__domicilio = value

    @sexo.setter
    def sexo(self, value: str):
        self.__sexo = value
    # endregion


class Usuario(Persona):
    # region Variables
    __acceso: TipoUsuario

    # endregion
    # region Operadores
    def __init__(self, email: str = "", nombre: str = "", apellido: str = "", apellido2: str = "", telefono: str = "",
                 edad: int = 0, fecha_nacimiento: date = None, domicilio: str = "", sexo: str = "",
                 acceso: TipoUsuario = TipoUsuario.NULL):
        super().__init__(email=email, nombre=nombre, apellido=apellido, apellido2=apellido2, telefono=telefono,
                         sexo=sexo, domicilio=domicilio, edad=edad, fecha_nacimiento=fecha_nacimiento)
        self.__acceso = acceso

    # endregion
    # region Getters
    @property
    def acceso(self) -> TipoUsuario:
        return self.__acceso

    # endregion
    # region Setters
    @acceso.setter
    def acceso(self, value: TipoUsuario):
        self.__acceso = value

    # endregion

class Cliente(Persona):
    # region Variables
    __pedidos: list

    # endregion
    # region Operadores
    def __init__(self, email: str = "", nombre: str = "", apellido: str = "", apellido2: str = "", telefono: str = "",
                 edad: int = 0, fecha_nacimiento: date = None, domicilio: str = "", sexo: str = "", id: int = -1):
        super().__init__(email=email, nombre=nombre, apellido=apellido, apellido2=apellido2, telefono=telefono,
                         sexo=sexo, domicilio=domicilio, edad=edad, fecha_nacimiento=fecha_nacimiento, id=id)
        self.__pedidos = []

    # endregion
    # region Getters

    # endregion
    # region Setters

    # endregion
    # region List
    def pedidos_len(self) -> int:
        return self.__pedidos.__len__()

    def get_item(self, pos: int):
        result = None
        if pos < self.__pedidos.__len__():
            result = self.__pedidos[pos]
        return result

    def remove_item(self, pos: int) -> bool:
        result = False
        if pos < self.__pedidos.__len__():
            del self.__pedidos[pos]
            result = True
        return result

    def delete_item(self, pos: int) -> bool:
        return self.remove_item(pos)

    def add_item(self, item):
        self.__pedidos.append(item)

    # endregion


