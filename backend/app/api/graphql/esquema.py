"""Esquema y resolvers GraphQL para consultar expedientes."""
from datetime import date, datetime

import strawberry
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from strawberry.fastapi import GraphQLRouter

from app.dependencias import obtener_servicio_auth, obtener_servicio_expedientes
from app.excepciones import CredencialesInvalidasError
from app.servicios.servicio_auth import ServicioAuth
from app.servicios.servicio_expedientes import ServicioExpedientes


@strawberry.type
class Diagnostico:
    id: int
    descripcion: str
    fecha: date


@strawberry.type
class Metrica:
    tipo: str
    valor: float
    timestamp: datetime


@strawberry.type
class Expediente:
    id: int
    paciente_id: int
    diagnosticos: list[Diagnostico]

    @strawberry.field
    def metricas(self, info: strawberry.Info, limite: int = 20) -> list[Metrica]:
        # MongoDB solo se consulta si el cliente pide este campo
        return info.context["servicio"].listar_metricas(self.paciente_id, limite)


@strawberry.type
class Query:
    @strawberry.field
    def expediente(self, info: strawberry.Info, paciente_id: int) -> Expediente:
        usuario = info.context["usuario"]
        if usuario is None:
            raise CredencialesInvalidasError("Falta el token")
        # Strawberry lee los campos de la entidad por su nombre
        return info.context["servicio"].obtener_expediente(paciente_id, usuario)


def obtener_contexto(
    credenciales: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
    servicio_auth: ServicioAuth = Depends(obtener_servicio_auth),
    servicio: ServicioExpedientes = Depends(obtener_servicio_expedientes),
) -> dict:
    # Sin token se puede abrir el editor de consultas, pero no consultar datos
    usuario = servicio_auth.usuario_desde_token(credenciales.credentials) if credenciales else None
    return {"usuario": usuario, "servicio": servicio}


router_graphql = GraphQLRouter(strawberry.Schema(query=Query), context_getter=obtener_contexto)
