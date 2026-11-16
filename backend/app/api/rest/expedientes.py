"""Endpoints de expedientes y diagnósticos."""
from fastapi import APIRouter, Depends

from app.api.schemas import DiagnosticoNuevo, ExpedienteSalida
from app.dependencias import medico_actual, obtener_servicio_expedientes, usuario_actual
from app.modelos import Medico, Usuario
from app.servicios.servicio_expedientes import ServicioExpedientes

router = APIRouter(prefix="/expedientes", tags=["Expedientes"])


@router.get("/{paciente_id}", response_model=ExpedienteSalida)
def obtener_expediente(
    paciente_id: int,
    usuario: Usuario = Depends(usuario_actual),
    servicio: ServicioExpedientes = Depends(obtener_servicio_expedientes),
):
    return servicio.obtener_expediente(paciente_id, usuario)


@router.post("/{paciente_id}/diagnosticos", response_model=ExpedienteSalida, status_code=201)
def agregar_diagnostico(
    paciente_id: int,
    datos: DiagnosticoNuevo,
    medico: Medico = Depends(medico_actual),
    servicio: ServicioExpedientes = Depends(obtener_servicio_expedientes),
):
    return servicio.agregar_diagnostico(paciente_id, datos.descripcion)
