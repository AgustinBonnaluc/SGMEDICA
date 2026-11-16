"""Lógica de negocio de expedientes y diagnósticos."""
from datetime import date

from app.excepciones import AccesoDenegadoError, NoEncontradoError
from app.modelos import Diagnostico, Expediente, MetricaSalud, Paciente, Usuario
from app.repositorios.interfaces import IRepositorioExpedientes, IRepositorioMetricas


class ServicioExpedientes:
    def __init__(
        self, repositorio: IRepositorioExpedientes, repositorio_metricas: IRepositorioMetricas
    ):
        self._repositorio = repositorio
        self._repositorio_metricas = repositorio_metricas

    def obtener_expediente(self, paciente_id: int, solicitante: Usuario) -> Expediente:
        # Un paciente solo puede ver su propio expediente
        if isinstance(solicitante, Paciente) and solicitante.id != paciente_id:
            raise AccesoDenegadoError("No se puede ver el expediente de otro paciente")
        return self._buscar_expediente(paciente_id)

    def agregar_diagnostico(self, paciente_id: int, descripcion: str) -> Expediente:
        expediente = self._buscar_expediente(paciente_id)
        expediente.agregar_diagnostico(Diagnostico(descripcion=descripcion, fecha=date.today()))
        return self._repositorio.guardar(expediente)

    def listar_metricas(self, paciente_id: int, limite: int) -> list[MetricaSalud]:
        return self._repositorio_metricas.listar_por_paciente(paciente_id, limite)

    def _buscar_expediente(self, paciente_id: int) -> Expediente:
        expediente = self._repositorio.buscar_por_paciente(paciente_id)
        if expediente is None:
            raise NoEncontradoError("El paciente no existe")
        return expediente
