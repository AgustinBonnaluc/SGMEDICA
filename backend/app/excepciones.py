"""Excepciones propias del negocio."""


class ReglaDeNegocioError(Exception):
    """Se intentó una operación que el negocio no permite."""
