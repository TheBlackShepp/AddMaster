from Enums import EtiquetaProducto
from Users import Cliente, date, IDClass


class Producto(IDClass):
    # region Variables
    __nombre: str
    __cantidad: int
    __precio: int
    __fecha_inicio_venta: date
    __fecha_fin_venta: date
    __etiquetas: list
    __descripcion: str

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


class Pedido(IDClass):
    # region Variables
    __cliente: Cliente
    __enviar_a_domicilio: bool
    __producto: Producto
    __fecha_entrega: date

    # endregion
    # region Operadores
    def __init__(self, cliente: Cliente, producto: Producto, enviar_a_domicilio: bool = False,
                 fecha_entrega: date = None, id: int = -1):
        super().__init__(id=id)
        self.__cliente = cliente
        self.__producto = producto
        self.__fecha_entrega = fecha_entrega
        self.__enviar_a_domicilio = enviar_a_domicilio

    # endregion
    # region Getters
    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def enviar_a_domicilio(self) -> bool:
        return self.__enviar_a_domicilio

    @property
    def fecha_entrega(self) -> date:
        return self.__fecha_entrega

    # endregion
    # region Setters
    @cliente.setter
    def cliente(self, value: Cliente):
        self.__cliente = value

    @producto.setter
    def producto(self, value: Producto):
        self.__producto = value

    @enviar_a_domicilio.setter
    def enviar_a_domicilio(self, value: bool):
        self.__enviar_a_domicilio = value

    @fecha_entrega.setter
    def fecha_entrega(self, value: date):
        self.__fecha_entrega = value

    # endregion


class PedidoDetalle(Pedido):
    # region Variables
    __fecha_compra: date
    __fecha_entregado: date

    # endregion
    # region Operadores
    def __init__(self, cliente: Cliente, producto: Producto, enviar_a_domicilio: bool = False,
                 fecha_entrega: date = None, id: int = -1, fecha_compra: date = None, fecha_entregado: date = None):
        super().__init__(cliente, producto, enviar_a_domicilio, fecha_entrega, id)
        self.__fecha_compra = fecha_compra
        self.__fecha_entregado = fecha_entregado

    # endregion
    # region Getters
    @property
    def fecha_compra(self) -> date:
        return self.__fecha_compra

    @property
    def fecha_entregado(self) -> date:
        return self.__fecha_entregado

    # endregion
    # region Setters
    @fecha_compra.setter
    def fecha_compra(self, value: date):
        self.__fecha_compra = value

    @fecha_entregado.setter
    def fecha_entregado(self, value: date):
        self.__fecha_entregado = value

    # endregion

