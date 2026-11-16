"""Excepciones propias del negocio."""


class ErrorDeNegocio(Exception):
    """Clase padre de los errores que la API traduce a una respuesta HTTP."""


class ReglaDeNegocioError(ErrorDeNegocio):
    """Se intentó una operación que el negocio no permite."""


class NoEncontradoError(ErrorDeNegocio):
    """El recurso pedido no existe."""


class CredencialesInvalidasError(ErrorDeNegocio):
    """El login o el token no son válidos."""


class AccesoDenegadoError(ErrorDeNegocio):
    """El usuario no tiene permiso sobre el recurso."""
