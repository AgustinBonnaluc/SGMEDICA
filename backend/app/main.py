"""Punto de entrada de la API principal."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import modelos  # noqa: F401 (registra las entidades antes de crear las tablas)
from app.api.rest import auth, citas, expedientes
from app.base_datos import Base, engine
from app.excepciones import (
    CredencialesInvalidasError,
    ErrorDeNegocio,
    NoEncontradoError,
    ReglaDeNegocioError,
)

Base.metadata.create_all(engine)

app = FastAPI(title="SGMEDICA")
app.include_router(auth.router)
app.include_router(citas.router)
app.include_router(expedientes.router)

ESTADOS_HTTP = {
    ReglaDeNegocioError: 400,
    CredencialesInvalidasError: 401,
    NoEncontradoError: 404,
}


@app.exception_handler(ErrorDeNegocio)
def manejar_error_de_negocio(request: Request, error: ErrorDeNegocio):
    return JSONResponse(status_code=ESTADOS_HTTP[type(error)], content={"detail": str(error)})
