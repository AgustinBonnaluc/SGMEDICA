"""Endpoints de autenticación."""
from fastapi import APIRouter, Depends

from app.api.schemas import Credenciales, MedicoNuevo, PacienteNuevo, Token, UsuarioSalida
from app.dependencias import obtener_servicio_auth
from app.servicios.servicio_auth import ServicioAuth

router = APIRouter(tags=["Autenticación"])


@router.post("/pacientes", response_model=UsuarioSalida, status_code=201)
def registrar_paciente(datos: PacienteNuevo, servicio: ServicioAuth = Depends(obtener_servicio_auth)):
    return servicio.registrar_paciente(**datos.model_dump())


@router.post("/medicos", response_model=UsuarioSalida, status_code=201)
def registrar_medico(datos: MedicoNuevo, servicio: ServicioAuth = Depends(obtener_servicio_auth)):
    return servicio.registrar_medico(**datos.model_dump())


@router.post("/login", response_model=Token)
def login(datos: Credenciales, servicio: ServicioAuth = Depends(obtener_servicio_auth)):
    return Token(access_token=servicio.login(datos.email, datos.password))
