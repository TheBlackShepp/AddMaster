from Herramientas.SimpleTools import DebugClass
from Pedido import Producto
from Users import Usuario, TipoUsuario
import json


class DatabaseController(DebugClass):
    __producto_list: list
    __user_list: list

    def __init__(self):
        self.__producto_list = []
        self.__user_list = []

        self.load_all()

    def load_all(self):
        try:
            with open('users.db') as json_file:
                data = json.loads(json.load(json_file))
                for user_data in data:
                    u = Usuario()
                    u.formulario(user_data)
                    self.__user_list.append(u)
        except:
            print("No hay file 'users.db' aun")
        try:
            with open('producto.db') as json_file:
                data = json.loads(json.load(json_file))
                for producto_data in data:
                    p = Producto()
                    p.formulario(producto_data)
                    self.__producto_list.append(p)
        except:
            print("No hay file 'producto.db' aun")

    def save_all(self):
        json_users = json.dumps([ob.__dict__() for ob in self.__user_list])
        json_productos = json.dumps([ob.__dict__() for ob in self.__producto_list])

        with open('users.db', 'w') as outfile:
            json.dump(json_users, outfile)

        with open('producto.db', 'w') as outfile:
            json.dump(json_productos, outfile)

    def modificar_datos_producto(self, id_producto: int, formulario: dict) -> bool:
        self._print((id_producto, formulario))
        result: bool = False
        if id_producto < self.__producto_list.__len__():
            result = True
            formulario.update({"id": self.__producto_list.__len__()})
            p = Producto()
            p.formulario(formulario)
            self.__producto_list[id_producto] = p
        return result

    def igresar_datos_producto(self, formulario: dict) -> None:
        formulario.update({"id": self.__producto_list.__len__()})
        p = Producto()
        p.formulario(formulario)
        self.__producto_list.append(p)

    def get_datos_producto(self, id_producto: int) -> dict:
        result: dict = {}
        if 0 <= id_producto < self.__producto_list.__len__():
            result.update(self.__producto_list[id_producto].__dict__())
        return result

    def user_permission(self, id_usuario: int) -> TipoUsuario:
        resultado = TipoUsuario.NULL
        if 0 <= id_usuario < self.__user_list.__len__():
            resultado = self.__user_list[id_usuario].acceso
        return resultado


"""d = DatabaseController()
d.igresar_datos_producto({
    "nombre": "Producto 1",
    "cantidad": 100,
    "precio": 1000,
    "fecha_inicio_venta": date.today().__str__(),
    "fecha_fin_venta": date.today().__str__(),
    "etiquetas": ["Etiqueta 1", "Etiqueta 2", "Etiqueta 3"],
    "descripcion": "No hay mucho que poner en un producto ficticio"
})
d.save_all()"""
