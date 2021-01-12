from Back.Enums import TipoMateria
from Back.Users import IDClass


class MateriaPrima(IDClass):
    # region Variables
    _tipo_materia: TipoMateria
    _cantidad: int

    # endregion
    # region Operadores
    def __init__(self, id: int = -1, tipo_materia: TipoMateria = TipoMateria.NULL, cantidad: int = -1):
        super().__init__(id=id)
        self._cantidad = cantidad
        self._tipo_materia = tipo_materia

    # endregion
    # region Getters
    @property
    def tipo_materia(self) -> TipoMateria:
        return self._tipo_materia

    @property
    def cantidad(self) -> int:
        return self._cantidad

    # endregion
    # region Setters
    @tipo_materia.setter
    def tipo_materia(self, value: TipoMateria):
        self._tipo_materia = value

    @cantidad.setter
    def cantidad(self, value: int):
        self._cantidad = value

    # endregion
    def formulario(self, formulario: dict):
        super(MateriaPrima, self).formulario(formulario)
        self._tipo_materia = formulario["tipo_materia"]
        self._cantidad = formulario["cantidad"]

    def __dict__(self) -> dict:
        dict_json: dict = super(MateriaPrima, self).__dict__()
        dict_json.update({
            "tipo_materia": self._tipo_materia.value,
            "cantidad": self._cantidad
        })
        return dict_json


class DetalleMateriaPrima(MateriaPrima):
    # region Variables
    _registro: dict    # str fecha_llegada: int(cantidad)
    _cantidad_recibida: int
    _fecha_llegada: str

    # endregion
    # region Operadores
    def __init__(self, id: int = -1, tipo_materia: TipoMateria = TipoMateria.NULL, cantidad: int = -1,
                 cantidad_recibida: int = -1, fecha_llegada: str = None):
        super().__init__(id, tipo_materia, cantidad)
        self._cantidad_recibida = cantidad_recibida
        self._fecha_llegada = fecha_llegada
        self._registro = {}

    # endregion
    # region Getters
    @property
    def cantidad_recibida(self) -> int:
        return self._cantidad_recibida

    @property
    def fecha_llegada(self) -> str:
        return self._fecha_llegada

    # endregion
    # region Setters
    @cantidad_recibida.setter
    def cantidad_recibida(self, value: int):
        self._cantidad_recibida = value

    @fecha_llegada.setter
    def fecha_llegada(self, value: str):
        self._fecha_llegada = value

    # endregion
    # region Dict
    def registro_len(self) -> int:
        return self._registro.__len__()

    def get_item(self, key: str) -> int:
        result: int = -1
        if self._registro.get(key) is not None:
            result = self._registro[key]
        return result

    def remove_item(self, key: str) -> bool:
        result = False
        if self._registro.get(key) is not None:
            del self._registro[key]
        return result

    def delete_item(self, key: str) -> bool:
        return self.remove_item(key)

    def add_item(self, key: str, cantidad: int):
        self._registro.update({key: cantidad})

    # endregion
    def formulario(self, formulario: dict):
        super(MateriaPrima, self).formulario(formulario)
        self._registro = formulario["registro"]
        self._cantidad_recibida = formulario["cantidad_recibida"]
        self._fecha_llegada = formulario["fecha_llegada"]

    def __dict__(self) -> dict:
        dict_json: dict = super(MateriaPrima, self).__dict__()
        dict_json.update({
            "registro": self._registro,
            "cantidad_recibida": self._cantidad_recibida,
            "fecha_llegada": self._fecha_llegada
        })
        return dict_json
