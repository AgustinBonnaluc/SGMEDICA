"""Conexiones a PostgreSQL y MongoDB."""
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import MONGO_URL, POSTGRES_URL

engine = create_engine(POSTGRES_URL)
# expire_on_commit=False: los objetos se pueden seguir leyendo después de guardar
SesionLocal = sessionmaker(bind=engine, expire_on_commit=False)

coleccion_metricas = MongoClient(MONGO_URL)["sgmedica"]["metricas_salud"]


class Base(DeclarativeBase):
    """Clase base de todas las entidades que se guardan en PostgreSQL."""
