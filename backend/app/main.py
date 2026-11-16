"""Punto de entrada de la API principal."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import modelos  # noqa: F401 (registra las entidades antes de crear las tablas)
from app.api.graphql.esquema import router_graphql
from app.api.rest import auth, citas, expedientes
from app.base_datos import Base, engine
from app.config import FRONTEND_URL
from app.excepciones import (
    AccesoDenegadoError,
    CredencialesInvalidasError,
    ErrorDeNegocio,
    NoEncontradoError,
    ReglaDeNegocioError,
)

Base.metadata.create_all(engine)

app = FastAPI(title="SGMEDICA")
# Permite que el frontend, servido desde otro origen, llame a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(citas.router)
app.include_router(expedientes.router)
app.include_router(router_graphql, prefix="/graphql")

ESTADOS_HTTP = {
    ReglaDeNegocioError: 400,
    CredencialesInvalidasError: 401,
    NoEncontradoError: 404,
    AccesoDenegadoError: 403,
}


@app.exception_handler(ErrorDeNegocio)
def manejar_error_de_negocio(request: Request, error: ErrorDeNegocio):
    return JSONResponse(status_code=ESTADOS_HTTP[type(error)], content={"detail": str(error)})
