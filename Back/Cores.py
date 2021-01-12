from Back.DatabaseController import DatabaseController
from Back.Enums import TipoCore, TipoUsuario
from Herramientas.SimpleTools import ControlVariables
from datetime import date


database_controller: DatabaseController = DatabaseController()


class CoreBase:
    # region Variables
    _control_variables: ControlVariables = ControlVariables()
    _params: str = "params"
    _permission: str = "permission"
    _resultado: str = "post_result"
    _tipo_de_core: TipoCore

    # endregion
    # region Funciones
    def user_have_permission(self, id_usuario: int) -> bool:
        """
        Nos indica si el usaurio puede acceder al sector de esta clase
        """
        resultado: bool = False
        if self._control_variables.variable_correcta_int(id_usuario) is False:
            resultado = False
        elif self._tipo_de_core == TipoCore.CoreReservas:
            tipo = database_controller.get_user_permission(id_usuario)
            resultado = tipo == TipoUsuario.Personal or tipo == TipoUsuario.Dolores
        elif self._tipo_de_core == TipoCore.CoreBodega:
            tipo = database_controller.get_user_permission(id_usuario)
            resultado = tipo == TipoUsuario.Administrativo or tipo == TipoUsuario.Dolores
        elif self._tipo_de_core == TipoCore.Sesion:
            resultado = True
        else:
            resultado = False
        return resultado

    def get_dict_params(self, value: bool) -> dict:
        return {self._params: value}

    def get_dict_permission(self, value: bool) -> dict:
        return {self._permission: value}

    def get_dict_resultado(self, value: bool) -> dict:
        return {self._resultado: value}

    def get_tipo_usuario(self, id_usuario: int) -> TipoUsuario:
        return database_controller.get_user_permission(id_usuario)

    def restore_form_id(self, formulario: dict) -> dict:
        if formulario.get('id') is not None:
            l: list = formulario.get('id')
            if l.__len__() > 0:
                formulario.update({"id": int(l[0])})
        return formulario

    def general_add(self, comprobador, funcion_de_generacion, id_usuario: int, formulario: dict):
        result: dict = {}
        if comprobador(formulario) and self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                funcion_de_generacion(formulario)
                result.update(self.get_dict_resultado(True))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result

    def general_delete(self, funcion_de_eliminacion, id_usuario: int, formulario: dict) -> dict:
        result: dict = {}
        formulario = self.restore_form_id(formulario)
        if formulario.get("id") is not None and \
                self._control_variables.variable_correcta_list_int([id_usuario, formulario["id"]]):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update(self.get_dict_resultado(funcion_de_eliminacion(formulario["id"])))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result

    def general_modify(self, comprobador, funcion_de_modificacion, id_usuario: int, formulario: dict):
        result: dict = {}
        formulario = self.restore_form_id(formulario)
        if comprobador(formulario) and self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update(self.get_dict_resultado(funcion_de_modificacion(formulario)))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result

    def general_get_datos(self, getter, id_usuario: int, formulario: dict) -> dict:
        result: dict = {}
        formulario = self.restore_form_id(formulario)
        if formulario.get("id") is not None and \
                self._control_variables.variable_correcta_list_int([id_usuario, formulario["id"]]):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = getter(formulario["id"])
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result

    def general_get_lists(self, getter, id_usuario: int) -> dict:
        """
        Obtiene los datos de todos los productos en una lista de diccionarios
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        result: dict = {}
        if self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = getter()
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result

    # endregion
    def __init__(self, tipo: TipoCore):
        self._tipo_de_core = tipo


class CoreReservas(CoreBase):
    # region Comprobaciones
    def comprobar_datos_producto(self, formulario: dict) -> bool:
        """
        Compruba si los datos del formulario recibido posee o no los dotos necesarios
        """
        li = ["id", "nombre", "cantidad", "precio", "fecha_inicio_venta", "fecha_fin_venta", "etiquetas", "descripcion"]
        return self._control_variables.contains_all_list_in_dict(formulario, li)

    def comprobar_datos_cliente(self, formulario: dict) -> bool:
        """
        Compruba si los datos del formulario recibido posee o no los dotos necesarios
        """
        li = ["id", "email", "nombre", "apellido", "apellido2", "telefono", "edad", "fecha_nacimiento", "domicilio",
              "sexo"]
        return self._control_variables.contains_all_list_in_dict(formulario, li)

    def comprobar_datos_pedido(self, formulario: dict) -> bool:
        """
        Compruba si los datos del formulario recibido posee o no los dotos necesarios
        """
        li = ["id", "id_cliente", "enviar_a_domicilio", "id_producto", "fecha_entrega", "fecha_compra",
              "fecha_entregado"]
        return self._control_variables.contains_all_list_in_dict(formulario, li)

    # endregion
    # region Producto
    def igresar_datos_producto(self, id_usuario: int, formulario: dict) -> dict:
        """
        Ingresa los datos de un producto
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        """result: dict = {}
        if self.comprobar_datos_producto(formulario) and self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                database_controller.igresar_datos_producto(formulario)
                result.update(self.get_dict_resultado(True))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return \
            self.general_add(
                self.comprobar_datos_producto, database_controller.igresar_datos_producto, id_usuario, formulario)

    def modificar_datos_producto(self, id_usuario: int, formulario: dict) -> dict:
        """
        Modifica los datos de un producto al core Reservas
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        """result: dict = {}
        self.restore_form_id(formulario)
        if self.comprobar_datos_producto(formulario) and self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update(self.get_dict_resultado(
                    database_controller.modificar_datos_producto(formulario)))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return \
            self.general_modify(
                self.comprobar_datos_cliente, database_controller.modificar_datos_producto, id_usuario, formulario)

    def get_datos_producto(self, id_usuario: int, formulario: dict) -> dict:
        """
        Obtiene los datos de un producto en un diccionario
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        self.restore_form_id(formulario)
        if formulario.get("id") is not None and \
                self._control_variables.variable_correcta_list_int([id_usuario, formulario["id"]]):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_datos_producto(formulario["id"])
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_datos(database_controller.get_datos_producto, id_usuario, formulario)

    def get_lista_productos(self, id_usuario: int) -> dict:
        """
        Obtiene los datos de todos los productos en una lista de diccionarios
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        if self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_lista_productos()
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_lists(database_controller.get_lista_productos, id_usuario)

    # endregion
    # region Cliente
    def dar_alta_cliente(self, id_usuario: int, formulario: dict) -> dict:
        """
        Añade un nuevo cliente a la lista
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        """result: dict = {}
        if self.comprobar_datos_cliente(formulario) and self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                database_controller.dar_alta_cliente(formulario)
                result.update(self.get_dict_resultado(True))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return \
            self.general_add(self.comprobar_datos_cliente, database_controller.dar_alta_cliente, id_usuario, formulario)

    def dar_baja_cliente(self, id_usuario: int, formulario: dict) -> dict:
        """
        Da de baja a un cliente
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se ha eliminado el cliente con exito
            post_result False: No se ha eliminado el cliente, ya que probablemente no exista
        """
        """result: dict = {}
        self.restore_form_id(formulario)
        if formulario.get("id") is not None and \
                self._control_variables.variable_correcta_list_int([id_usuario, formulario["id"]]):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update(self.get_dict_resultado(
                    database_controller.dar_baja_cliente(formulario["id"])))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_delete(database_controller.dar_baja_cliente, id_usuario, formulario)

    def modificar_datos_cliente(self, id_usuario: int, formulario: dict):
        """
        Modifica los datos de un cliente
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        """result: dict = {}
        self.restore_form_id(formulario)
        if self.comprobar_datos_cliente(formulario) and self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update(self.get_dict_resultado(
                    database_controller.modificar_datos_cliente(formulario)))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return \
            self.general_modify(
                self.comprobar_datos_cliente, database_controller.modificar_datos_cliente, id_usuario, formulario)

    def get_datos_cliente(self, id_usuario: int, formulario: dict) -> dict:
        """
        Obtiene los datos de un cliente
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        self.restore_form_id(formulario)
        if formulario.get("id") is not None and \
                self._control_variables.variable_correcta_list_int([id_usuario, formulario["id"]]):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_datos_cliente(formulario["id"])
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_datos(database_controller.get_datos_cliente, id_usuario, formulario)

    def get_lista_clientes(self, id_usuario: int) -> dict:
        """
        Obtiene los datos de todos los productos en una lista de diccionarios
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        if self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_lista_clientes()
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_lists(database_controller.get_lista_clientes, id_usuario)

    # endregion
    # region Pedido Detalle
    def igresar_datos_pedido(self, id_usuario: int, formulario: dict) -> dict:
        """
        Ingresa los datos de un pedido
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        """result: dict = {}
        if self.comprobar_datos_pedido(formulario) and self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                database_controller.igresar_datos_pedido(formulario)
                result.update(self.get_dict_resultado(True))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return \
            self.general_add(
                self.comprobar_datos_pedido, database_controller.igresar_datos_pedido, id_usuario, formulario)

    def eliminar_pedido(self, id_usuario: int, formulario: dict) -> dict:
        """
        Modifica los datos de un pedido
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        """result: dict = {}
        if self.comprobar_datos_pedido(formulario) and self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update(self.get_dict_resultado(
                    database_controller.modificar_datos_pedido(formulario)))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_delete(database_controller.eliminar_pedido, id_usuario, formulario)

    def modificar_datos_pedido(self, id_usuario: int, formulario: dict) -> dict:
        return \
            self.general_modify(
                self.comprobar_datos_cliente, database_controller.modificar_datos_pedido, id_usuario, formulario)

    def get_datos_pedido(self, id_usuario: int, formulario: dict) -> dict:
        """
        Obtiene los datos de un producto en un diccionario
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        if self._control_variables.variable_correcta_list_int([id_usuario, id_producto]):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_datos_producto(id_producto)
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_datos(database_controller.get_datos_pedido, id_usuario, formulario)

    def get_lista_pedidos(self, id_usuario: int) -> dict:
        """
        Obtiene los datos de todos los productos en una lista de diccionarios
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        if self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_lista_productos()
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_lists(database_controller.get_lista_pedidos, id_usuario)

    # endregion
    def __init__(self):
        super().__init__(TipoCore.CoreReservas)


class CoreBodega(CoreBase):
    # region Comprobaciones
    def comprobar_datos_usuario(self, id_usuario: int, formulario: dict) -> bool:
        """
        Compruba si los datos del formulario recibido posee o no los dotos necesarios
        """
        li: list = []
        if id_usuario == 0:
            li = ["id", "email", "nombre", "apellido", "apellido2", "telefono", "edad", "fecha_nacimiento", "domicilio",
                  "sexo", "acceso"]
        else:
            li = ["id", "email", "nombre", "apellido", "apellido2", "telefono", "edad", "fecha_nacimiento", "domicilio",
                  "sexo"]
        return self._control_variables.contains_all_list_in_dict(formulario, li)

    def comprobar_datos_materia_prima(self, formulario: dict) -> bool:
        """
        Compruba si los datos del formulario recibido posee o no los dotos necesarios
        """
        li = ["id", "tipo_materia", "cantidad", "registro", "cantidad_recibida", "fecha_llegada"]
        return self._control_variables.contains_all_list_in_dict(formulario, li)

    # endregion
    # region Usuarios
    def ingresar_usuario(self, id_usuario: int, formulario: dict) -> dict:
        """
        Añade un nuevo cliente a la lista
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        """result: dict = {}
        # Si es un usuario valido
        if self._control_variables.variable_correcta_int(id_usuario) and \
                self.comprobar_datos_usuario(id_usuario, formulario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                database_controller.add_new_user(id_usuario, formulario)
                result.update(self.get_dict_resultado(True))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return \
            self.general_add(
                self.comprobar_datos_usuario, database_controller.add_new_user, id_usuario, formulario)

    def eliminar_usuario(self, id_usuario: int, formulario: dict) -> dict:
        """
        Elimina un usuario de la base de datos
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se ha eliminado el cliente con exito
            post_result False: No se ha eliminado el cliente, ya que probablemente no exista
        """
        """result: dict = {}
        self.restore_form_id(formulario)
        if formulario.get("id") is not None and \
                self._control_variables.variable_correcta_list_int([id_usuario, formulario["id"]]):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update(self.get_dict_resultado(
                    database_controller.remove_user(formulario["id"])))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_delete(database_controller.remove_user, id_usuario, formulario)

    def modificar_usuario(self, id_usuario: int, formulario: dict):
        """
        Modifica los datos de un usuario
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        """result: dict = {}
        self.restore_form_id(formulario)
        if self.comprobar_datos_usuario(id_usuario, formulario) and \
                self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                result.update(self.get_dict_resultado(
                    database_controller.modificar_datos_user(id_usuario, formulario)))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return \
            self.general_modify(
                self.comprobar_datos_usuario, database_controller.modificar_datos_user, id_usuario, formulario)

    def get_datos_usuario(self, id_usuario: int, formulario: dict) -> dict:
        """
        Obtiene los datos de un usuario
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        self.restore_form_id(formulario)
        if self._control_variables.variable_correcta_int(id_usuario) and \
                self.comprobar_datos_usuario(id_usuario, formulario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_datos_user(formulario["id"])
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_datos(database_controller.get_datos_user, id_usuario, formulario)

    def get_lista_usuarios(self, id_usuario: int) -> dict:
        """
        Obtiene los datos de todos los productos en una lista de diccionarios
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        if self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_lista_user()
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_lists(database_controller.get_lista_user, id_usuario)

    # endregion
    # region Detalle Materia Prima
    def igresar_datos_materia_prima(self, id_usuario: int, formulario: dict) -> dict:
        """
        Ingresa los datos de un producto
        Precondicion: EL usuario no puede ser -1, sino devuelve que no puede acceder aqui
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se han creado o modificado los datos de un producto
            post_result False: No se han creado o modificado los datos de un producto
        """
        """result: dict = {}
        if self.comprobar_datos_materia_prima(formulario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                database_controller.igresar_datos_materia_prima(formulario)
                result.update(self.get_dict_resultado(True))
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_add(
            self.comprobar_datos_materia_prima, database_controller.igresar_datos_materia_prima, id_usuario, formulario)

    def eliminar_meteria_prima(self, id_usuario: int, formulario: dict) -> dict:
        """
        Elimina un usuario de la base de datos
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
            post_result True: Se ha eliminado el cliente con exito
            post_result False: No se ha eliminado el cliente, ya que probablemente no exista
        """
        return self.general_delete(database_controller.eliminar_materia_prima, id_usuario, formulario)

    def get_datos_materia_prima(self, id_usuario: int, formulario: dict) -> dict:
        """
        Obtiene los datos de una materia prima en un diccionario
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        if self._control_variables.variable_correcta_int(id_usuario) and self.form_to_id(formulario) != -1:
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_datos_materia_prima(self.form_to_id(formulario))
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_datos(database_controller.get_datos_materia_prima, id_usuario, formulario)

    def get_lista_materia_prima(self, id_usuario: int) -> dict:
        """
        Obtiene los datos de todos las materias primas en una lista de diccionarios
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        if self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_lista_materia_prima()
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_lists(database_controller.get_lista_materia_prima, id_usuario)

    def get_lista_materias_primas(self, id_usuario: int) -> dict:
        """
        Obtiene los datos de todos los productos en una lista de diccionarios
        Segun los datos recibidos:
            permission True: Se puede acceder a esta funcionalidad con el id_persona
            permission False: No se puede acceder a esta funcionalidad con el id_persona
            params True: Los datos recibidos estan en formato correcto
            params False: Los datos recibidos no estan en formato correcto
        """
        """result: dict = {}
        if self._control_variables.variable_correcta_int(id_usuario):
            result.update(self.get_dict_params(True))
            if self.user_have_permission(id_usuario):
                result.update(self.get_dict_permission(True))
                d = database_controller.get_lista_user()
                if d.__len__() == 0:
                    result.update(self.get_dict_params(False))
                else:
                    result.update(d)
            else:
                result.update(self.get_dict_permission(False))
        else:
            result.update(self.get_dict_params(False))
        return result"""
        return self.general_get_lists(database_controller.get_lista_materia_prima, id_usuario)

    # endregion
    def __init__(self):
        super().__init__(TipoCore.CoreBodega)


class CoreSeesion(CoreBase):
    def __init__(self):
        super().__init__(TipoCore.Sesion)

    def comprobar_inicio_sesion(self, formulario: dict) -> bool:
        """
        Compruba si los datos del formulario recibido posee o no los dotos necesarios
        """
        li = ["email", "password"]
        return self._control_variables.contains_all_list_in_dict(formulario, li)

    def iniciar_sesion(self, formulario: dict) -> int:
        """
        Inicia sesion
        Devuelve el id del usuario
        Devuelve -1 si no existe
        """
        result: int = -1
        if self.comprobar_inicio_sesion(formulario):
            result = database_controller.comprobar_user_credentials(formulario)
        return result


productoTest1 = {
    'id': 0,
    'nombre': 'Producto 1 modificado',
    'cantidad': 999,
    "precio": 100,
    'fecha_inicio_venta': '2021-01-09',
    'fecha_fin_venta': '2021-01-09',
    'etiquetas': ['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3'],
    'descripcion': 'No hay mucho que poner en un producto ficticio'
}
clienteTest = {
    "id": 0,
    "email": "clienteTest1@gmail.com",
    "nombre": "Nombre Cliente",
    "apellido": "Apellido 1",
    "apellido2": "Apellido 2",
    "telefono": "666666666",
    "edad": 99,
    "fecha_nacimiento": date.today().__str__(),
    "domicilio": "None",
    "sexo": "X"
}
usuarioTest = {
    "id": 0,

    "email": "usuarioTest@gmail.com",
    "nombre": "Nombre Usuario Administrativo",
    "apellido": "Apellido 1",
    "apellido2": "Apellido 2",
    "telefono": "666666666",
    "edad": 99,
    "fecha_nacimiento": date.today().__str__(),
    "domicilio": "None",
    "sexo": "X",
    
    "acceso": TipoUsuario.Administrativo.value,
    "password": "Password1"
}


"""
c_s = CoreSeesion()
print(f'ID: {c_s.iniciar_sesion({"email": "dolores@gmail.com", "password": "Password1"})}')
print(f'Tipo usaurio: {c_s.get_tipo_usuario(0)}')
"""
#c_r = CoreReservas()
# region Tests Productos
#print("Producto:", c_r.igresar_datos_producto(0, productoTest1))  # {'params': True, 'permission': True, 'post_result': True}
#print("Producto:", c_r.get_datos_producto(0, 0))    # {'params': True, 'permission': True, 'id': 0, 'nombre': 'Producto 1 modificado', 'cantidad': 999, 'precio': 100, 'fecha_inicio_venta': '2021-01-09', 'fecha_fin_venta': '2021-01-09', 'etiquetas': ['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3'], 'descripcion': 'No hay mucho que poner en un producto ficticio'}
#print("Producto:", c_r.get_datos_producto(0, 1))    # {'params': False, 'permission': True}
"""
productoTest1.update({"nombre": "Producto 1 renamed"})
print("Result:", c_r.modificar_datos_producto(0, productoTest1))  # {'params': True, 'permission': True, 'id': 0, 'nombre': 'Producto 1 renamed', 'cantidad': 999, 'precio': 100, 'fecha_inicio_venta': '2021-01-09', 'fecha_fin_venta': '2021-01-09', 'etiquetas': ['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3'], 'descripcion': 'No hay mucho que poner en un producto ficticio'}
print("Producto:", c_r.get_datos_producto(0, 0))
"""
# print("Resultado:", c_r.get_lista_productos(0))
# endregion
# region Tests Clientes
"""
print("Cliente: ", c_r.get_datos_cliente(0, 0))
print("Alta: ", c_r.dar_alta_cliente(0, clienteTest))
print("Cliente: ", c_r.get_datos_cliente(0, 0))
"""
"""
print("Alta: ", c_r.dar_alta_cliente(0, clienteTest))
clienteTest.update({"nombre": "Cliente a eliminar"})
print("Alta: ", c_r.dar_alta_cliente(0, clienteTest))
print("Cliente: ", c_r.get_datos_cliente(0, 0))
print("Cliente: ", c_r.get_datos_cliente(0, 1))
print("Result: ", c_r.dar_baja_cliente(0, 1))
"""
"""
print("Alta: ", c_r.dar_alta_cliente(0, clienteTest))
print("Alta: ", c_r.dar_alta_cliente(0, clienteTest))
print("Result: ", c_r.dar_baja_cliente(0, 1))
print("Result: ", c_r.dar_baja_cliente(0, 1))
"""
# print("Cliente: ", c_r.get_datos_cliente(0, 0))
"""
clienteTest.update({"nombre": "Cliente a eliminar"})
print("Modify: ", c_r.modificar_datos_cliente(0, clienteTest))
"""
# endregion

#c_b = CoreBodega()
# region Personal
"""#print("Ingreso: ", c_b.ingresar_usuario(0, usuarioTest))
# print("Eliminado", c_b.eliminar_personal(0, 3))
print("User: ", c_b.get_datos_usuario(0, 1))
usuarioTest.update({"id": 1})
usuarioTest.update({"apellido2": "Willyx"})
print("Modificar: ", c_b.modificar_usuario(0, usuarioTest))
print("User: ", c_b.get_datos_usuario(0, 1))"""
# endregion


#database_controller.save_all()

"""
print(c.get_datos_producto(0, 0))
print(c.modificar_datos_producto(0, 0, {
    "nombre": "Producto 1 modificado",
    "cantidad": 999,
    "precio": 1,
    "fecha_inicio_venta": date.today().__str__(),
    "fecha_fin_venta": date.today().__str__(),
    "etiquetas": ["Etiqueta 1", "Etiqueta 2", "Etiqueta 3"],
    "descripcion": "No hay mucho que poner en un producto ficticio"
}))"""
"""print(c.dar_alta_cliente(0, {
    "email": "emailtest",
    "nombre": "Pato",
    "apellido": "Willyx",
    "apellido2": "Mixta",
    "telefono": "666666666",
    "edad": 2,
    "fecha_nacimiento": date.today().__str__(),
    "domicilio": "Noooo!",
    "sexo": "M"
}))"""

