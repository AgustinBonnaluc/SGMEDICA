"""Lógica de negocio de expedientes y diagnósticos."""
from datetime import date

from app.excepciones import NoEncontradoError
from app.modelos import Diagnostico, Expediente
from app.repositorios.interfaces import IRepositorioExpedientes


class ServicioExpedientes:
    def __init__(self, repositorio: IRepositorioExpedientes):
        self._repositorio = repositorio

    def obtener_expediente(self, paciente_id: int) -> Expediente:
        expediente = self._repositorio.buscar_por_paciente(paciente_id)
        if expediente is None:
            raise NoEncontradoError("El paciente no existe")
        return expediente

    def agregar_diagnostico(self, paciente_id: int, descripcion: str) -> Expediente:
        expediente = self.obtener_expediente(paciente_id)
        expediente.agregar_diagnostico(Diagnostico(descripcion=descripcion, fecha=date.today()))
        return self._repositorio.guardar(expediente)
