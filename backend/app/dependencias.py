"""Inyección de dependencias: único lugar que conoce las clases concretas."""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.base_datos import SesionLocal
from app.modelos import Medico, Paciente, Usuario
from app.repositorios.repositorio_citas_postgres import RepositorioCitasPostgres
from app.repositorios.repositorio_expedientes_postgres import RepositorioExpedientesPostgres
from app.repositorios.repositorio_usuarios_postgres import RepositorioUsuariosPostgres
from app.servicios.servicio_auth import ServicioAuth
from app.servicios.servicio_citas import ServicioCitas
from app.servicios.servicio_expedientes import ServicioExpedientes


def obtener_sesion():
    with SesionLocal() as sesion:
        yield sesion


def obtener_servicio_auth(sesion: Session = Depends(obtener_sesion)) -> ServicioAuth:
    return ServicioAuth(RepositorioUsuariosPostgres(sesion))


def obtener_servicio_citas(sesion: Session = Depends(obtener_sesion)) -> ServicioCitas:
    return ServicioCitas(RepositorioCitasPostgres(sesion), RepositorioUsuariosPostgres(sesion))


def obtener_servicio_expedientes(sesion: Session = Depends(obtener_sesion)) -> ServicioExpedientes:
    return ServicioExpedientes(RepositorioExpedientesPostgres(sesion))


def usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    servicio: ServicioAuth = Depends(obtener_servicio_auth),
) -> Usuario:
    return servicio.usuario_desde_token(credenciales.credentials)


def paciente_actual(usuario: Usuario = Depends(usuario_actual)) -> Paciente:
    if not isinstance(usuario, Paciente):
        raise HTTPException(status_code=403, detail="Solo disponible para pacientes")
    return usuario


def medico_actual(usuario: Usuario = Depends(usuario_actual)) -> Medico:
    if not isinstance(usuario, Medico):
        raise HTTPException(status_code=403, detail="Solo disponible para médicos")
    return usuario
