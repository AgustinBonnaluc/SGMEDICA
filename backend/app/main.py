"""Punto de entrada de la API principal."""
from fastapi import FastAPI

from app import modelos  # noqa: F401 (registra las entidades antes de crear las tablas)
from app.base_datos import Base, engine

Base.metadata.create_all(engine)

app = FastAPI(title="SGMEDICA")
