"""Acceso a usuarios en PostgreSQL."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modelos import Usuario
from app.repositorios.interfaces import IRepositorioUsuarios


class RepositorioUsuariosPostgres(IRepositorioUsuarios):
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def guardar(self, usuario: Usuario) -> Usuario:
        self._sesion.add(usuario)
        self._sesion.commit()
        return usuario

    def buscar_por_id(self, id: int) -> Usuario | None:
        return self._sesion.get(Usuario, id)

    def buscar_por_email(self, email: str) -> Usuario | None:
        return self._sesion.scalar(select(Usuario).where(Usuario.email == email))
