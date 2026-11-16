"""Conexiones a PostgreSQL y MongoDB."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import POSTGRES_URL

engine = create_engine(POSTGRES_URL)
# expire_on_commit=False: los objetos se pueden seguir leyendo después de guardar
SesionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Clase base de todas las entidades que se guardan en PostgreSQL."""
