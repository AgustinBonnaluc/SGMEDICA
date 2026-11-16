"""Acceso a expedientes y diagnósticos en PostgreSQL."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modelos import Expediente
from app.repositorios.interfaces import IRepositorioExpedientes


class RepositorioExpedientesPostgres(IRepositorioExpedientes):
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def guardar(self, expediente: Expediente) -> Expediente:
        self._sesion.add(expediente)
        self._sesion.commit()
        return expediente

    def buscar_por_paciente(self, paciente_id: int) -> Expediente | None:
        return self._sesion.scalar(select(Expediente).where(Expediente.paciente_id == paciente_id))
