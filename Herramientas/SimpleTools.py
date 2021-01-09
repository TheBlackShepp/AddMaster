class DebugClass:
    """
    Clase preparada para que cualquier clase la herede
    Al activar el modo debug, las funciones de esta clase se ejecutan
    Si se tiene desactivado, pasan como si no existiesen
    """
    __debug_mode: bool = False

    @property
    def _debug_mode(self) -> bool:
        return self.__debug_mode

    @_debug_mode.setter
    def _debug_mode(self, debug: bool):
        self.__debug_mode = debug

    def _print(self, something):
        """
        Printea algo si esta en modo debug
        """
        if self.__debug_mode:
            print(something)


class ControlVariables:
    """
    Clase especializada en analizar variables basicas
    Se suele usar como control de variables para permitir o no el paso a otras funcionalidades
    """
    # region Control de variables
    def variable_correcta(self, var: str) -> bool:
        """
        Nos devuelve true si un string no esta vacio(len: 0) y no es None
        """
        if var is None:
            resultado = False
        elif var.__len__() == 0:
            resultado = False
        else:
            resultado = True
        return resultado

    def variable_correcta_int(self, var: int) -> bool:
        """
        Devuelve true si el numero es mayor o igual a 0 y no es None
        """
        if var is None:
            resultado = False
        elif var < 0:
            resultado = False
        else:
            resultado = True
        return resultado

    def variable_correcta_list(self, var: list) -> bool:
        """
        Usa en una lista de string la funcion variable_correcta()
        Devuelve true si todas las string contenidas son validas
        """
        if var is None:
            resultado = False
        elif var.__len__() == 0:
            resultado = False
        else:
            resultado = True
            for i in var:
                resultado = self.variable_correcta(i)
                if resultado is False:
                    break
        return resultado

    def variable_correcta_list_int(self, var: list) -> bool:
        """
        Usa en una lista de ints la funcion variable_correcta_int()
        Devuelve true si todas los valores contenidos son validas
        """
        if var is None:
            resultado = False
        elif var.__len__() == 0:
            resultado = False
        else:
            resultado = True
            for i in var:
                resultado = self.variable_correcta_int(i)
                if resultado is False:
                    break
        return resultado

    def remove_null_from_list(self, var: list) -> int:
        """
        Elimina de una lista de strings todos los strings no validos segun la funcion variable_correcta()
        Para eliminar los elemetos usa la funcion remove_from_list()
        Al final devuelve el numero de elementos eleiminados
        """
        return self.remove_from_list(var, self.variable_correcta)

    def remove_from_list(self, var: list, func) -> int:
        """
        Elimina todas las variables de una lista segun una funcion de comparacion
        La funcion debe de poder recibir un elemento de la lista y devolver True si es valido o false si se quiere eliminar
        Al final devuelve el numero de elementos eleiminados
        """
        borrados: int = 0
        for i in range(0, var.__len__()):
            if type(var[i - borrados]) == str:
                if func(var[i - borrados]) is False:
                    del var[i - borrados]
                    borrados += 1
        return borrados

    def start_witn_num(self, var: str) -> bool:
        """
        Nos devuelve True si un string recibido tiene un numero en el primer caracter
        -No comprueba si el string es un string valido o no-
        """
        resultado: bool = False
        if self.variable_correcta(var) is True:
            if var[0].isnumeric():
                resultado = True
        return resultado

    def string_is_numeric(self, var: str) -> bool:
        """
        Nos devuelve si un string es un numero o no(True o False)
        Si el string esta vacio o es None devuelve False por defecto
        """
        resultado: bool = False
        if self.variable_correcta(var) is True:
            if var.isnumeric():
                resultado = True
        return resultado

    def string_is_float(self, var: str) -> bool:
        """
        Separa un string por '.', y si ambas substring son numericas devuelve True
        Si el string no es valido devuelve False segun la funcion variable_correcta()
        **Devuelve False si posee mas de un '.'
        """
        resultado: bool = False
        if self.variable_correcta(var) is True:
            if var.__contains__('.') is True:
                sep: list = var.split('.')
                if sep.__len__() == 2:
                    if self.string_is_numeric(sep[0]) and self.string_is_numeric(sep[1]):
                        resultado = True
        return resultado

    def contains_any(self, string: str, list_strings: list) -> int:
        """
        Devuelve la posicion del string de la lista que esta contenido en el string
        Si el string no esta en la lista devuelve -1
        """
        resultado: int = -1
        for i in range(0, list_strings.__len__()):
            if string.__contains__(list_strings[i]):
                resultado = i
                break
        return resultado

    def contains_all_list_in_dict(self, d: dict, li: list) -> bool:
        """
        Comprueba si un diccionario contiene todas las keys nombradas en una lista
        """
        result: bool = True
        for i in li:
            if d.__contains__(i) is False:
                result = False
                break
        return result

    # endregion
