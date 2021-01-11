from Back.Enums import EtiquetaProducto
from Back.Users import Cliente, IDClass


class Producto(IDClass):
    # region Variables
    _nombre: str
    _cantidad: int
    _precio: int
    _fecha_inicio_venta: str
    _fecha_fin_venta: str
    _etiquetas: list
    _descripcion: str

    # endregion
    # region Operadores
    def __init__(self, id: int = -1, nombre: str = "", cantidad: int = -1, precio: int = -1,
                 fecha_inicio_venta: str = "", fecha_fin_venta: str = "", descripcion: str = ""):
        super().__init__(id=id)
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
        self._fecha_inicio_venta = fecha_inicio_venta
        self._fecha_fin_venta = fecha_fin_venta
        self._descripcion = descripcion
        self._etiquetas = []

    # endregion
    # region Getters
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def precio(self) -> int:
        return self._precio

    @property
    def fecha_inicio_venta(self) -> str:
        return self._fecha_inicio_venta

    @property
    def fecha_fin_venta(self) -> str:
        return self._fecha_fin_venta

    @property
    def descripcion(self) -> str:
        return self._descripcion

    # endregion
    # region Setters
    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

    @cantidad.setter
    def cantidad(self, value: int):
        self._cantidad = value

    @precio.setter
    def precio(self, value: int):
        self._precio = value

    @fecha_inicio_venta.setter
    def fecha_inicio_venta(self, value: str):
        self._fecha_inicio_venta = value

    @fecha_fin_venta.setter
    def fecha_fin_venta(self, value: str):
        self._fecha_fin_venta = value

    @descripcion.setter
    def descripcion(self, value: str):
        self._descripcion = value

    # endregion
    # region List
    def etiquetas_len(self) -> int:
        return self._etiquetas.__len__()

    def get_item(self, pos: int) -> EtiquetaProducto:
        result: EtiquetaProducto = EtiquetaProducto.NULL
        if pos < self._etiquetas.__len__():
            result = self._etiquetas[pos]
        return result

    def remove_item(self, pos: int) -> bool:
        result = False
        if pos < self._etiquetas.__len__():
            del self._etiquetas[pos]
            result = True
        return result

    def delete_item(self, pos: int) -> bool:
        return self.remove_item(pos)

    def add_item(self, item: EtiquetaProducto):
        self._etiquetas.append(item)

    # endregion
    def formulario(self, formulario: dict):
        super(Producto, self).formulario(formulario)
        self._nombre = formulario["nombre"]
        self._cantidad = formulario["cantidad"]
        self._fecha_inicio_venta = formulario["fecha_inicio_venta"]
        self._fecha_fin_venta = formulario["fecha_fin_venta"]
        self._etiquetas = formulario["etiquetas"]
        self._descripcion = formulario["descripcion"]

    def __dict__(self) -> dict:
        dict_json: dict = super(Producto, self).__dict__()
        dict_json.update({
            "nombre": self._nombre,
            "cantidad": self._cantidad,
            "fecha_inicio_venta": self._fecha_inicio_venta,
            "fecha_fin_venta": self._fecha_fin_venta,
            "etiquetas": self._etiquetas,
            "descripcion": self._descripcion
        })
        return dict_json


class Pedido(IDClass):
    # region Variables
    _cliente: Cliente
    _enviar_a_domicilio: bool
    _producto: Producto
    _fecha_entrega: str

    # endregion
    # region Operadores
    def __init__(self, cliente: Cliente, producto: Producto, enviar_a_domicilio: bool = False,
                 fecha_entrega: str = "", id: int = -1):
        super().__init__(id=id)
        self._cliente = cliente
        self._producto = producto
        self._fecha_entrega = fecha_entrega
        self._enviar_a_domicilio = enviar_a_domicilio

    # endregion
    # region Getters
    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def producto(self) -> Producto:
        return self._producto

    @property
    def enviar_a_domicilio(self) -> bool:
        return self._enviar_a_domicilio

    @property
    def fecha_entrega(self) -> str:
        return self._fecha_entrega

    # endregion
    # region Setters
    @cliente.setter
    def cliente(self, value: Cliente):
        self._cliente = value

    @producto.setter
    def producto(self, value: Producto):
        self._producto = value

    @enviar_a_domicilio.setter
    def enviar_a_domicilio(self, value: bool):
        self._enviar_a_domicilio = value

    @fecha_entrega.setter
    def fecha_entrega(self, value: str):
        self._fecha_entrega = value

    # endregion
    def formulario(self, formulario: dict):
        super(Pedido, self).formulario(formulario)
        self._cliente = Cliente()
        self._cliente.formulario(formulario["cliente"])
        self._enviar_a_domicilio = formulario["enviar_a_domicilio"]
        self._producto = Producto()
        self._producto.formulario(formulario["producto"])
        self._fecha_entrega = formulario["fecha_entrega"]

    def __dict__(self) -> dict:
        dict_json: dict = super(Pedido, self).__dict__()
        dict_json.update({
            "cliente": self._cliente.__dict__(),
            "enviar_a_domicilio": self._enviar_a_domicilio,
            "producto": self._producto.__dict__(),
            "fecha_entrega": self._fecha_entrega
        })
        return dict_json


class PedidoDetalle(Pedido):
    # region Variables
    _fecha_compra: str
    _fecha_entregado: str

    # endregion
    # region Operadores
    def __init__(self, cliente: Cliente, producto: Producto, enviar_a_domicilio: bool = False,
                 fecha_entrega: str = "", id: int = -1, fecha_compra: str = "", fecha_entregado: str = ""):
        super().__init__(cliente, producto, enviar_a_domicilio, fecha_entrega, id)
        self._fecha_compra = fecha_compra
        self._fecha_entregado = fecha_entregado

    # endregion
    # region Getters
    @property
    def fecha_compra(self) -> str:
        return self._fecha_compra

    @property
    def fecha_entregado(self) -> str:
        return self._fecha_entregado

    # endregion
    # region Setters
    @fecha_compra.setter
    def fecha_compra(self, value: str):
        self._fecha_compra = value

    @fecha_entregado.setter
    def fecha_entregado(self, value: str):
        self._fecha_entregado = value

    # endregion
    def formulario(self, formulario: dict):
        super(PedidoDetalle, self).formulario(formulario)
        self._fecha_compra = formulario["fecha_compra"]
        self._fecha_entregado = formulario["fecha_entregado"]

    def __dict__(self) -> dict:
        dict_json: dict = super(Pedido, self).__dict__()
        dict_json.update({
            "fecha_compra": self._fecha_compra,
            "fecha_entregado": self._fecha_entregado
        })
        return dict_json

    def imprimir(self):
        return "Contenido del pedido detalle a imprimir"