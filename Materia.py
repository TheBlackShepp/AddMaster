from Enums import TipoMateria
from Users import IDClass


class MateriaPrima(IDClass):
    # region Variables
    __tipo_materia: TipoMateria
    __cantidad: int

    # endregion
    # region Operadores
    def __init__(self, id: int = -1, nombre: str = "", cantidad: int = -1, precio: int = -1,
                 fecha_inicio_venta: date = None, fecha_fin_venta: date = None, descripcion: str = ""):
        super().__init__(id=id)
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio
        self.__fecha_inicio_venta = fecha_inicio_venta
        self.__fecha_fin_venta = fecha_fin_venta
        self.__descripcion = descripcion
        self.__etiquetas = []

    # endregion
    # region Getters
    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def precio(self) -> int:
        return self.__precio

    @property
    def fecha_inicio_venta(self) -> date:
        return self.__fecha_inicio_venta

    @property
    def fecha_fin_venta(self) -> date:
        return self.__fecha_fin_venta

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    # endregion
    # region Setters
    @nombre.setter
    def nombre(self, value: str):
        self.__nombre = value

    @cantidad.setter
    def cantidad(self, value: int):
        self.__cantidad = value

    @precio.setter
    def precio(self, value: int):
        self.__precio = value

    @fecha_inicio_venta.setter
    def fecha_inicio_venta(self, value: date):
        self.__fecha_inicio_venta = value

    @fecha_fin_venta.setter
    def fecha_fin_venta(self, value: date):
        self.__fecha_fin_venta = value

    @descripcion.setter
    def descripcion(self, value: str):
        self.__descripcion = value

    # endregion
    # region List
    def etiquetas_len(self) -> int:
        return self.__etiquetas.__len__()

    def get_item(self, pos: int) -> EtiquetaProducto:
        result: EtiquetaProducto = EtiquetaProducto.NULL
        if pos < self.__etiquetas.__len__():
            result = self.__etiquetas[pos]
        return result

    def remove_item(self, pos: int) -> bool:
        result = False
        if pos < self.__etiquetas.__len__():
            del self.__etiquetas[pos]
            result = True
        return result

    def delete_item(self, pos: int) -> bool:
        return self.remove_item(pos)

    def add_item(self, item: EtiquetaProducto):
        self.__etiquetas.append(item)

    # endregion

