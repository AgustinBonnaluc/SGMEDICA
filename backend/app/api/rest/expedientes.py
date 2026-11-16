"""Endpoints de expedientes y diagnósticos."""
from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas import DiagnosticoNuevo, ExpedienteSalida
from app.dependencias import medico_actual, obtener_servicio_expedientes, usuario_actual
from app.modelos import Medico, Paciente, Usuario
from app.servicios.servicio_expedientes import ServicioExpedientes

router = APIRouter(prefix="/expedientes", tags=["Expedientes"])


@router.get("/{paciente_id}", response_model=ExpedienteSalida)
def obtener_expediente(
    paciente_id: int,
    usuario: Usuario = Depends(usuario_actual),
    servicio: ServicioExpedientes = Depends(obtener_servicio_expedientes),
):
    # Un paciente solo puede ver su propio expediente
    if isinstance(usuario, Paciente) and usuario.id != paciente_id:
        raise HTTPException(status_code=403, detail="No se puede ver el expediente de otro paciente")
    return servicio.obtener_expediente(paciente_id)


@router.post("/{paciente_id}/diagnosticos", response_model=ExpedienteSalida, status_code=201)
def agregar_diagnostico(
    paciente_id: int,
    datos: DiagnosticoNuevo,
    medico: Medico = Depends(medico_actual),
    servicio: ServicioExpedientes = Depends(obtener_servicio_expedientes),
):
    return servicio.agregar_diagnostico(paciente_id, datos.descripcion)
