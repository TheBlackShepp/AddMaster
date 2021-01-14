from enum import Enum


class EtiquetaProducto(Enum):
    NULL = -1


class TipoUsuario(Enum):
    NULL = -1
    Dolores = 0
    Personal = 1
    Administrativo = 2


class TipoMateria(Enum):
    NULL = -1
    Alvarinio = 0
    Verdejo = 1
    Chanrdonnay = 2
    Tempranillo = 3


class TipoCore(Enum):
    NULL = -1
    CoreReservas = 0
    CoreBodega = 1
    Sesion = 2
