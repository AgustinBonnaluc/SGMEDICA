"""Endpoints de citas."""
from fastapi import APIRouter, Depends

from app.api.schemas import CitaNueva, CitaSalida
from app.dependencias import medico_actual, obtener_servicio_citas, paciente_actual, usuario_actual
from app.modelos import Medico, Paciente, Usuario
from app.servicios.servicio_citas import ServicioCitas

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.post("", response_model=CitaSalida, status_code=201)
def agendar_cita(
    datos: CitaNueva,
    paciente: Paciente = Depends(paciente_actual),
    servicio: ServicioCitas = Depends(obtener_servicio_citas),
):
    return servicio.agendar_cita(paciente.id, datos.medico_id, datos.fecha)


@router.get("", response_model=list[CitaSalida])
def listar_mis_citas(
    paciente: Paciente = Depends(paciente_actual),
    servicio: ServicioCitas = Depends(obtener_servicio_citas),
):
    return servicio.listar_por_paciente(paciente.id)


@router.post("/{cita_id}/confirmar", response_model=CitaSalida)
def confirmar_cita(
    cita_id: int,
    medico: Medico = Depends(medico_actual),
    servicio: ServicioCitas = Depends(obtener_servicio_citas),
):
    return servicio.confirmar_cita(cita_id, medico.id)


@router.post("/{cita_id}/cancelar", response_model=CitaSalida)
def cancelar_cita(
    cita_id: int,
    usuario: Usuario = Depends(usuario_actual),
    servicio: ServicioCitas = Depends(obtener_servicio_citas),
):
    return servicio.cancelar_cita(cita_id, usuario.id)
