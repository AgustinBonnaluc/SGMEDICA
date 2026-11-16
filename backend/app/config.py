"""Configuración leída desde variables de entorno."""
import os

# Los valores por defecto sirven para trabajar en local
POSTGRES_URL = os.getenv(
    "POSTGRES_URL", "postgresql+psycopg://sgmedica:sgmedica@localhost:5432/sgmedica"
)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27018")
JWT_SECRETO = os.getenv("JWT_SECRETO", "secreto-solo-para-desarrollo-local")
JWT_ALGORITMO = "HS256"
JWT_MINUTOS_DE_VIDA = 60
