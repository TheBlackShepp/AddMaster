from Herramientas.SimpleTools import DebugClass, ControlVariables
from Back.Pedido import Producto
from Back.Users import Usuario, TipoUsuario, Cliente
from json import load, loads, dump, dumps
from hashlib import sha3_512


class DatabaseController(DebugClass):
    # region Variables
    __control_variables: ControlVariables = ControlVariables()
    __producto_list: list
    __last_producto_id: int
    __user_list: list
    __last_user_id: int
    __client_list: list
    __last_client_id: int

    # endregion
    # region Funciones
    def __init__(self):
        self.__producto_list = []
        self.__user_list = []
        self.__client_list = []
        self.__last_producto_id = 0
        self.__last_user_id = 0
        self.__last_client_id = 0
        self.load_all()

    def load_all(self):
        try:
            with open('users.db') as json_file:
                data = loads(load(json_file))
                self.__last_user_id = data['id']
                data = data['users']
                for user_data in data:
                    u = Usuario()
                    u.formulario(user_data)
                    self.__user_list.append(u)
        except:
            print("No hay file 'users.db' aun")
        try:
            with open('producto.db') as json_file:
                data = loads(load(json_file))
                self.__last_producto_id = data['id']
                data = data['products']
                for producto_data in data:
                    p = Producto()
                    p.formulario(producto_data)
                    self.__producto_list.append(p)
        except:
            print("No hay file 'producto.db' aun")
        try:
            with open('clients.db') as json_file:
                data = loads(load(json_file))
                self.__last_client_id = data['id']
                data = data['clients']
                for client_data in data:
                    c = Cliente()
                    c.formulario(client_data)
                    self.__producto_list.append(c)
        except:
            print("No hay file 'clients.db' aun")

    def save_all(self):
        json_users = dumps({"users": [ob.__dict__() for ob in self.__user_list], "id": self.__last_user_id})
        json_productos = \
            dumps({"products": [ob.__dict__() for ob in self.__producto_list], "id": self.__last_producto_id})
        json_clients = dumps({"clients": [ob.__dict__() for ob in self.__client_list], "id": self.__last_client_id})

        with open('users.db', 'w') as outfile:
            dump(json_users, outfile)
        with open('producto.db', 'w') as outfile:
            dump(json_productos, outfile)
        with open('clients.db', 'w') as outfile:
            dump(json_clients, outfile)

    def get_pos_id_object(self, id_object: int, l: list) -> int:
        result: int = -1
        for i in range(l.__len__()):
            if l[i].id == id_object:
                result = i
                break
        return result

    # endregion
    # region Productos
    def igresar_datos_producto(self, formulario: dict) -> None:
        formulario.update({"id": self.__last_producto_id})
        self.__last_producto_id += 1
        p = Producto()
        p.formulario(formulario)
        self.__producto_list.append(p)

    def modificar_datos_producto(self, id_producto: int, formulario: dict) -> bool:
        result: bool = False
        pos: int = self.get_pos_id_producto(id_producto)
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            formulario.update({"id": id_producto})
            self.__producto_list[pos].formulario(formulario)
        return result

    def get_datos_producto(self, id_producto: int) -> dict:
        result: dict = {}
        pos: int = self.get_pos_id_producto(id_producto)
        if self.__control_variables.variable_correcta_int(pos):
            result.update(self.__producto_list[pos].__dict__())
        return result

    def get_lista_productos(self) -> dict:
        temp_list: list = []
        for i in self.__producto_list:
            temp_list.append(i.__dict__())
        return {"productos": temp_list}

    def get_pos_id_producto(self, id_producto: int) -> int:
        return self.get_pos_id_object(id_producto, self.__producto_list)

    # endregion
    # region Clientes
    def dar_alta_cliente(self, formulario: dict) -> None:
        formulario.update({"id": self.__last_client_id})
        self.__last_client_id += 1
        c = Cliente()
        c.formulario(formulario)
        self.__client_list.append(c)

    def dar_baja_cliente(self, id_cliente: int) -> bool:
        result: bool = False
        pos: int = self.get_pos_id_client(id_cliente)
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            del self.__client_list[pos]
        return result

    def modificar_datos_cliente(self, id_cliente: int, formulario: dict) -> bool:
        result: bool = False
        pos: int = self.get_pos_id_client(id_cliente)
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            formulario.update({"id": id_cliente})
            self.__client_list[pos].formulario(formulario)
        return result

    def get_datos_cliente(self, id_cliente: int) -> dict:
        result: dict = {}
        pos: int = self.get_pos_id_client(id_cliente)
        if self.__control_variables.variable_correcta_int(pos):
            result.update(self.__client_list[pos].__dict__())
        return result

    def get_pos_id_client(self, id_cliente: int) -> int:
        return self.get_pos_id_object(id_cliente, self.__client_list)

    # endregion
    # region Users
    def add_new_user(self, formulario: dict) -> None:
        """
        Creamos un usuario con los paramentros recibidos
        Si no se reciben los apramentros correctos dara ERROR
        La password la recibe en claro y la transforma a sha512
        """
        formulario.update({"id": self.__last_user_id})
        formulario.update({"password": sha3_512(formulario['password'].encode()).hexdigest()})
        u = Usuario()
        u.formulario(formulario)
        self.__user_list.append(u)
        self.__last_user_id += 1

    def remove_user(self, id_usuario: int) -> bool:
        """
        Borra cualquier usuario menos el usuario 0 cual es el de Dolores
        Devuelve si ha eliminado el usuario o no
        """
        result: bool = False
        if id_usuario != 0:
            pos: int = self.get_pos_id_user(id_usuario)
            if self.__control_variables.variable_correcta_int(pos):
                result = True
                del self.__user_list[pos]
        return result

    def modificar_datos_user(self, id_usuario: int, formulario: dict) -> bool:
        """
        Modifica cualquier dato de un usuario menos la contraseña
        Devuelve si se han modificado los datos
        """
        result: bool = False
        pos: int = self.get_pos_id_user(id_usuario)
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            formulario.update({"id": id_usuario})
            old_pass: str = self.__user_list[pos]
            self.__user_list[pos].formulario(formulario)
            self.__user_list[pos].password = old_pass
        return result

    def get_pos_id_user(self, id_usuario: int) -> int:
        return self.get_pos_id_object(id_usuario, self.__user_list)

    def get_user_permission(self, id_usuario: int) -> TipoUsuario:
        result = TipoUsuario.NULL
        pos: int = self.get_pos_id_user(id_usuario)
        if self.__control_variables.variable_correcta_int(pos):
            result = self.__user_list[pos].acceso
        return result

    def comprobar_user_credentials(self, formulario: dict) -> bool:
        result: bool = False
        for i in self.__user_list:
            if i.same_credentials(formulario):
                result = True
                break
        return result

    # endregion



"""d = DatabaseController()
d.save_all()
self.add_new_user({
    "email": "dolore@gmail.com",
    "nombre": "DOlores",
    "apellido": "Willyx",
    "apellido2": "Mixta",
    "telefono": "666666666",
    "edad": 2,
    "fecha_nacimiento": date.today().__str__(),
    "domicilio": "Noooo!",
    "sexo": "F",
    "password": "Password1",
    "acceso": TipoUsuario.Dolores.value
})"""
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
d.save_all()
"""