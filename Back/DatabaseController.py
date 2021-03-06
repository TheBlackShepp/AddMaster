from Herramientas.SimpleTools import DebugClass, ControlVariables
from Back.Pedido import Producto, PedidoDetalle
from Back.Users import Usuario, TipoUsuario, Cliente
from Back.Materia import DetalleMateriaPrima
from json import load, loads, dump, dumps
from hashlib import sha3_512


class DatabaseController(DebugClass):
    # region Variables
    __control_variables: ControlVariables = ControlVariables()
    __producto_list: list
    __last_producto_id: int
    __producto_name: str = "products"

    __user_list: list
    __last_user_id: int
    __user_name: str = "users"

    __client_list: list
    __last_client_id: int
    __client_name: str = "clients"

    __materia_prima_list: list
    __last_materia_prima_id: int
    __materia_prima_name: str = "materias"

    __pedido_list: list
    __last_pedido_id: int
    __pedido_name: str = "pedido"

    # endregion
    # region Funciones
    def __init__(self):
        self.__producto_list = []
        self.__last_producto_id = 0

        self.__user_list = []
        self.__last_user_id = 0

        self.__client_list = []
        self.__last_client_id = 0

        self.__materia_prima_list = []
        self.__last_materia_prima_id = 0

        self.__pedido_list = []
        self.__last_pedido_id = 0

        self.load_all()

    def load_all(self):
        try:
            with open(f'{self.__user_name}.db') as json_file:
                data = loads(load(json_file))
                self.__last_user_id = data['id']
                data = data[self.__user_name]
                for user_data in data:
                    u = Usuario()
                    u.formulario(user_data)
                    self.__user_list.append(u)
        except:
            print(f"No hay file '{self.__user_name}.db' aun")
        try:
            with open(f'{self.__producto_name}.db') as json_file:
                data = loads(load(json_file))
                self.__last_producto_id = data['id']
                data = data[self.__producto_name]
                for producto_data in data:
                    p = Producto()
                    p.formulario(producto_data)
                    self.__producto_list.append(p)
        except:
            print(f"No hay file '{self.__producto_name}.db' aun")
        try:
            with open(f'{self.__client_name}.db') as json_file:
                data = loads(load(json_file))
                self.__last_client_id = data['id']
                data = data[self.__client_name]
                for client_data in data:
                    c = Cliente()
                    c.formulario(client_data)
                    self.__client_list.append(c)
        except:
            print(f"No hay file '{self.__client_name}.db' aun")
        try:
            with open(f'{self.__materia_prima_name}.db') as json_file:
                data = loads(load(json_file))
                self.__last_materia_prima_id = data['id']
                data = data[self.__materia_prima_name]
                for materia_prima_data in data:
                    m = DetalleMateriaPrima()
                    m.formulario(materia_prima_data)
                    self.__materia_prima_list.append(m)
        except:
            print(f"No hay file '{self.__materia_prima_name}.db' aun")
        try:
            with open(f'{self.__pedido_name}.db') as json_file:
                data = loads(load(json_file))
                self.__last_pedido_id = data['id']
                data = data[self.__pedido_name]
                for pedido_detalle_data in data:
                    m = PedidoDetalle()
                    m.formulario(pedido_detalle_data)
                    self.__pedido_list.append(m)
        except:
            print(f"No hay file '{self.__pedido_name}.db' aun")

    def save_all(self):
        self.save_productos()
        self.save_users()
        self.save_clients()
        self.save_materias()
        self.save_pedidos()

    def save_productos(self):
        json_productos = \
            dumps({self.__producto_name: [ob.__dict__() for ob in self.__producto_list], "id": self.__last_producto_id})
        with open(f'{self.__producto_name}.db', 'w') as outfile:
            dump(json_productos, outfile)

    def save_users(self):
        json_users = \
            dumps({self.__user_name: [ob.__dict__() for ob in self.__user_list], "id": self.__last_user_id})
        with open(f'{self.__user_name}.db', 'w') as outfile:
            dump(json_users, outfile)

    def save_clients(self):
        json_clients = \
            dumps({self.__client_name: [ob.__dict__() for ob in self.__client_list], "id": self.__last_client_id})
        with open(f'{self.__client_name}.db', 'w') as outfile:
            dump(json_clients, outfile)

    def save_materias(self):
        json_materias = \
            dumps({self.__materia_prima_name: [ob.__dict__() for ob in self.__materia_prima_list], "id": self.__last_materia_prima_id})
        with open(f'{self.__materia_prima_name}.db', 'w') as outfile:
            dump(json_materias, outfile)

    def save_pedidos(self):
        json_pedidos = \
            dumps({self.__pedido_name: [ob.__dict__() for ob in self.__pedido_list], "id": self.__last_pedido_id})
        with open(f'{self.__pedido_name}.db', 'w') as outfile:
            dump(json_pedidos, outfile)

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
        p = Producto()
        p.formulario(formulario)
        self.__producto_list.append(p)
        self.__last_producto_id += 1
        self.save_productos()

    def modificar_datos_producto(self, formulario: dict) -> bool:
        result: bool = False
        pos: int = self.get_pos_id_producto(formulario["id"])
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            self.__producto_list[pos].formulario(formulario)
            self.save_productos()
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
        return {self.__producto_name: temp_list}

    def get_pos_id_producto(self, id_producto: int) -> int:
        return self.get_pos_id_object(id_producto, self.__producto_list)

    # endregion
    # region Clientes
    def dar_alta_cliente(self, formulario: dict) -> None:
        formulario.update({"id": self.__last_client_id})
        formulario.update({"pedidos": []})
        c = Cliente()
        c.formulario(formulario)
        self.__client_list.append(c)
        self.__last_client_id += 1
        self.save_clients()

    def dar_baja_cliente(self, id_cliente: int) -> bool:
        result: bool = False
        pos: int = self.get_pos_id_client(id_cliente)
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            del self.__client_list[pos]
            self.save_clients()
        return result

    def modificar_datos_cliente(self, formulario: dict) -> bool:
        result: bool = False
        pos: int = self.get_pos_id_client(formulario["id"])
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            formulario.update({"pedidos": self.__client_list[pos].pedidos})
            self.__client_list[pos].formulario(formulario)
            self.save_clients()
        return result

    def get_datos_cliente(self, id_cliente: int) -> dict:
        result: dict = {}
        pos: int = self.get_pos_id_client(id_cliente)
        if self.__control_variables.variable_correcta_int(pos):
            result.update(self.__client_list[pos].__dict__())
        return result

    def get_lista_clientes(self) -> dict:
        temp_list: list = []
        for i in self.__client_list:
            temp_list.append(i.__dict__())
        return {self.__client_name: temp_list}

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
        # Si el que añade el usuario no es dolores, el usuario creado es de tipo Administrativo siempre
        if formulario["creator"] != 0:
            formulario.update({"acceso": TipoUsuario.Personal.value})
        formulario.update({"id": self.__last_user_id})
        
        print(type(formulario['password']), formulario['password'])
        
        formulario.update({"password": sha3_512(formulario['password'].encode()).hexdigest()})
        u = Usuario()
        u.formulario(formulario)
        self.__user_list.append(u)
        self.__last_user_id += 1
        self.save_users()

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
                self.save_users()
        return result

    def modificar_datos_user(self, formulario: dict) -> bool:
        """
        Modifica cualquier dato de un usuario menos la contraseña
        Devuelve si se han modificado los datos
        """
        result: bool = False
        pos: int = self.get_pos_id_user(formulario["id"])
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            old_pass: str = self.__user_list[pos].password
            old_tipo: int = self.__user_list[pos].acceso.value
            self.__user_list[pos].formulario(formulario)
            self.__user_list[pos].password = old_pass
            # Si el usuario que ha intentado cambiar los permisis es dolores
            # Hacemos que se mantengan
            # En caso contrario, los restauramos a los anteriores
            if formulario["creator"] != 0:
                self.__user_list[pos].acceso = TipoUsuario(old_tipo)
            self.save_users()
        return result

    def get_datos_user(self, id_usuario: int) -> dict:
        result: dict = {}
        pos: int = self.get_pos_id_user(id_usuario)
        if self.__control_variables.variable_correcta_int(pos):
            result.update(self.__user_list[pos].__dict__())
        return result

    def get_pos_id_user(self, id_usuario: int) -> int:
        return self.get_pos_id_object(id_usuario, self.__user_list)

    def get_lista_user(self) -> dict:
        temp_list: list = []
        for i in self.__user_list:
            d: dict = i.__dict__()
            d["password"] = None
            temp_list.append(d)
        return {self.__user_name: temp_list}

    def get_user_permission(self, id_usuario: int) -> TipoUsuario:
        result = TipoUsuario.NULL
        pos: int = self.get_pos_id_user(id_usuario)
        if self.__control_variables.variable_correcta_int(pos):
            result = self.__user_list[pos].acceso
        return result

    def comprobar_user_credentials(self, formulario: dict) -> int:
        result: int = -1
        formulario.update({"password": sha3_512(formulario['password'].encode()).hexdigest()})
        for i in range(self.__user_list.__len__()):
            if self.__user_list[i].same_credentials(formulario):
                result = self.__user_list[i].id
                break
        return result

    # endregion
    # region Pedido Detalle
    def igresar_datos_pedido(self, formulario: dict) -> None:
        formulario.update({"id": self.__last_pedido_id})
        p = PedidoDetalle()
        p.formulario(formulario)
    
        self.__pedido_list.append(p)
        self.__last_pedido_id += 1
        self.save_pedidos()

    def modificar_datos_pedido(self, formulario: dict) -> bool:
        result: bool = False
        pos: int = self.get_pos_id_pedido(formulario["id"])
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            self.__pedido_list[pos].formulario(formulario)
            self.save_pedidos()
        return result

    def eliminar_pedido(self, id_pedido_detalle: int) -> bool:
        result: bool = False
        pos: int = self.get_pos_id_pedido(id_pedido_detalle)
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            del self.__pedido_list[pos]
            self.save_pedidos()
        return result

    def get_datos_pedido(self, id_pedido_detalle: int) -> dict:
        result: dict = {}
        pos: int = self.get_pos_id_pedido(id_pedido_detalle)
        if self.__control_variables.variable_correcta_int(pos):
            result.update(self.__pedido_list[pos].__dict__())
        return result

    def get_lista_pedidos(self) -> dict:
        temp_list: list = []
        for i in self.__pedido_list:
            temp_list.append(i.__dict__())
        return {self.__pedido_name: temp_list}

    def get_pos_id_pedido(self, id_pedido_detalle: int) -> int:
        return self.get_pos_id_object(id_pedido_detalle, self.__pedido_list)

    # endregion
    # region Materia Prima
    def igresar_datos_materia_prima(self, formulario: dict) -> None:
        formulario.update({"id": self.__last_materia_prima_id})
        m = DetalleMateriaPrima()
        m.formulario(formulario)
        self.__materia_prima_list.append(m)
        self.__last_materia_prima_id += 1
        self.save_materias()

    def modificar_datos_materia_prima(self, formulario: dict) -> bool:
        result: bool = False
        pos: int = self.get_pos_id_materia_prima(formulario["id"])
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            self.__materia_prima_list[pos].formulario(formulario)
            self.save_materias()
        return result

    def eliminar_materia_prima(self, id_materia_prima: int) -> bool:
        result: bool = False
        pos: int = self.get_pos_id_materia_prima(id_materia_prima)
        if self.__control_variables.variable_correcta_int(pos):
            result = True
            del self.__materia_prima_list[pos]
            self.save_materias()
        return result

    def get_datos_materia_prima(self, id_materia_prima: int) -> dict:
        result: dict = {}
        pos: int = self.get_pos_id_materia_prima(id_materia_prima)
        if self.__control_variables.variable_correcta_int(pos):
            result.update(self.__materia_prima_list[pos].__dict__())
        return result

    def get_lista_materia_prima(self) -> dict:
        temp_list: list = []
        for i in self.__materia_prima_list:
            temp_list.append(i.__dict__())
        return {self.__materia_prima_name: temp_list}

    def get_pos_id_materia_prima(self, id_materia_prima: int) -> int:
        return self.get_pos_id_object(id_materia_prima, self.__materia_prima_list)

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