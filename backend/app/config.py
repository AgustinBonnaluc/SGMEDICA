"""Configuración leída desde variables de entorno."""
import os

# El valor por defecto coincide con .env.example para trabajar en local
POSTGRES_URL = os.getenv(
    "POSTGRES_URL", "postgresql+psycopg://sgmedica:sgmedica@localhost:5432/sgmedica"
)
