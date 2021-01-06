from pymysql import Connection, connect, MySQLError
from SimpleTools import DebugClass


class BaseDatos(DebugClass):
    # region Variables de la clase
    __port: int
    __data_base: str
    __host_name: str
    __username: str
    __password: str
    __connect_time_out: int = 5
    __connector: Connection
    __conexion__iniciada: bool
    __notconected: str = "Conecxion con la base de datos no realizada"

    # endregion
    # region Funciones
    def connect(self) -> bool:
        """
        Se requiere para poder hacer consultas
        Se conecta a la base de datos segun los datos dados al inicio
        Si no puede devuelve False y deja la clase como no iniciada(Se puede reintentar usar connect para conectarse)

        Si se reutiliza cuando la clase ya habia sido iniciada no hace nada, no reconecta.
        """
        if self.__conexion__iniciada is False:
            try:
                self.__connector = connect(host=self.__host_name, port=3306, user=self.__username,
                                                   passwd=self.__password, db=self.__data_base,
                                                   connect_timeout=self.__connect_time_out)
                self.__conexion__iniciada = True
            except MySQLError as e:
                self.__conexion__iniciada = False
                print(e)
        return self.__conexion__iniciada

    @property
    def conexion_iniciada(self) -> bool:
        return self.__conexion__iniciada

    def update(self, consulta: str, parametros: dict) -> int:
        """
        Realiza la funcion update/create en la base de datos

        Si devuelve:
        -2: No estaba realizada la conexion a la DB por lo que no se ha hecho nada
        -1: Ha habido un error en la consulta
         N: Se han realizado N cambios en la DB
        """
        self._print(consulta)
        self._print(parametros)
        resultado: int = 0
        if self.__conexion__iniciada:
            with self.__connector.cursor() as cursor:
                try:
                    resultado = cursor.execute(consulta, parametros)
                    self.__connector.commit()
                except MySQLError as m:
                    print(m)
                    resultado = -1
        else:
            resultado = -2
            self._print(self.__notconected)
        return resultado

    def select_count(self, consulta: str, parametros: dict) -> int:
        """
        Realiza un select y devuelve el numero de casos recibidos

        Si devuelve:
        -2: No estaba realizada la conexion a la DB por lo que no se ha hecho nada
        -1: Ha habido un error en la consulta
         N: Han habido N resultados segun la consulta
        """
        self._print(consulta)
        self._print(parametros)
        if self.__conexion__iniciada:
            with self.__connector.cursor() as cursor:
                try:
                    cursor.execute(consulta, parametros)
                    resultado = cursor.rowcount
                except MySQLError as m:
                    print(m)
                    resultado = -1
        else:
            resultado = -2
            self._print(self.__notconected)
        return resultado

    def select(self, consulta: str, parametros: dict) -> list and int:
        """
        Realiza un select y devuelve una lista de los resultados: la tabla resultante

        Si devuelve una lista y un numero con el valor:
        -2: No estaba realizada la conexion a la DB por lo que no se ha hecho nada
        -1 None: Ha habido un error en la consulta
         0: Tabla resultante de la consulta esta en la lista
        """
        self._print(consulta)
        self._print(parametros)
        resultado: list = []
        result: int = 0
        if self.__conexion__iniciada:
            with self.__connector.cursor() as cursor:
                try:
                    cursor.execute(consulta, parametros)
                    for row in cursor:
                        res: list = []
                        for colum in row:
                            res.append(colum)
                        resultado.append(res)
                except MySQLError as m:
                    print(m)
                    result = -1
        else:
            result = -2
            self._print(self.__notconected)
        return resultado, result

    # endregion
    def __init__(self, database: str, host_name: str, username: str, password: str,
                 connect_timeout: int = 5, port: int = 3306, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.__port = port
        self.__database = database
        self.__host_name = host_name
        self.__username = username
        self.__password = password
        self.__connect_time_out = connect_timeout
        self.__conexion__iniciada = False
