from Enums import TipoUsuario
from datetime import date


class IDClass:
    # region Variables
    _id: int

    # endregion
    # region Operadores
    def __init__(self, id: int = -1):
        self._id = id

    # endregion
    # region Getters
    @property
    def id(self) -> int:
        return self._id

    # endregion
    # region Setters
    @id.setter
    def id(self, value: int):
        self._id = value

    # endregion


class Persona(IDClass):
    # region Variables
    _email: str
    _nombre: str
    _apellido: str
    _apellido2: str
    _telefono: str
    _edad: int
    _fecha_nacimiento: date
    _domicilio: str
    _sexo: str

    # endregion
    # region Operadores
    def __init__(self, email: str = "", nombre: str = "", apellido: str = "", apellido2: str = "", telefono: str = "",
                 edad: int = 0, fecha_nacimiento: date = None, domicilio: str = "", sexo: str = "", id: int = -1):
        super().__init__(id=id)
        self._email = email
        self._nombre = nombre
        self._apellido = apellido
        self._apellido2 = apellido2
        self._telefono = telefono
        self._edad = edad
        self._fecha_nacimiento = fecha_nacimiento
        self._domicilio = domicilio
        self._sexo = sexo

    # endregion
    # region Getters
    @property
    def email(self) -> str:
        return self._email

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellido(self) -> str:
        return self._apellido

    @property
    def apellido2(self) -> str:
        return self._apellido2

    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def edad(self) -> int:
        return self._edad

    @property
    def fecha_nacimiento(self) -> date:
        return self._fecha_nacimiento

    @property
    def domicilio(self) -> str:
        return self._domicilio

    @property
    def sexo(self) -> str:
        return self._sexo

    # endregion
    # region Setters
    @email.setter
    def email(self, value: str):
        self._email = value

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

    @apellido.setter
    def apellido(self, value: str):
        self._apellido = value

    @apellido2.setter
    def apellido2(self, value: str):
        self._apellido2 = value

    @telefono.setter
    def telefono(self, value: str):
        self._telefono = value

    @edad.setter
    def edad(self, value: int):
        self._edad = value

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, value: date):
        self._fecha_nacimiento = value

    @domicilio.setter
    def domicilio(self, value: str):
        self._domicilio = value

    @sexo.setter
    def sexo(self, value: str):
        self._sexo = value

    # endregion


class Usuario(Persona):
    # region Variables
    _acceso: TipoUsuario

    # endregion
    # region Operadores
    def __init__(self, email: str = "", nombre: str = "", apellido: str = "", apellido2: str = "", telefono: str = "",
                 edad: int = 0, fecha_nacimiento: date = None, domicilio: str = "", sexo: str = "",
                 acceso: TipoUsuario = TipoUsuario.NULL):
        super().__init__(email=email, nombre=nombre, apellido=apellido, apellido2=apellido2, telefono=telefono,
                         sexo=sexo, domicilio=domicilio, edad=edad, fecha_nacimiento=fecha_nacimiento)
        self._acceso = acceso

    # endregion
    # region Getters
    @property
    def acceso(self) -> TipoUsuario:
        return self._acceso

    # endregion
    # region Setters
    @acceso.setter
    def acceso(self, value: TipoUsuario):
        self._acceso = value

    # endregion


class Cliente(Persona):
    # region Variables
    _pedidos: list

    # endregion
    # region Operadores
    def __init__(self, email: str = "", nombre: str = "", apellido: str = "", apellido2: str = "", telefono: str = "",
                 edad: int = 0, fecha_nacimiento: date = None, domicilio: str = "", sexo: str = "", id: int = -1):
        super().__init__(email=email, nombre=nombre, apellido=apellido, apellido2=apellido2, telefono=telefono,
                         sexo=sexo, domicilio=domicilio, edad=edad, fecha_nacimiento=fecha_nacimiento, id=id)
        self._pedidos = []

    # endregion
    # region Getters

    # endregion
    # region Setters

    # endregion
    # region List
    def pedidos_len(self) -> int:
        return self._pedidos.__len__()

    def get_item(self, pos: int):
        result = None
        if pos < self._pedidos.__len__():
            result = self._pedidos[pos]
        return result

    def remove_item(self, pos: int) -> bool:
        result = False
        if pos < self._pedidos.__len__():
            del self._pedidos[pos]
            result = True
        return result

    def delete_item(self, pos: int) -> bool:
        return self.remove_item(pos)

    def add_item(self, item):
        self._pedidos.append(item)

    # endregion


