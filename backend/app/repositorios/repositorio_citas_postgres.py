"""Acceso a citas en PostgreSQL."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modelos import Cita
from app.repositorios.interfaces import IRepositorioCitas


class RepositorioCitasPostgres(IRepositorioCitas):
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def guardar(self, cita: Cita) -> Cita:
        self._sesion.add(cita)
        self._sesion.commit()
        return cita

    def buscar_por_id(self, id: int) -> Cita | None:
        return self._sesion.get(Cita, id)

    def listar_por_paciente(self, paciente_id: int) -> list[Cita]:
        consulta = select(Cita).where(Cita.paciente_id == paciente_id).order_by(Cita.fecha)
        return list(self._sesion.scalars(consulta))
