"""Esquemas Pydantic de entrada y salida de la API."""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, NaiveDatetime


class PacienteNuevo(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=6, max_length=50)
    fecha_nacimiento: date


class MedicoNuevo(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=6, max_length=50)
    matricula: str = Field(min_length=1, max_length=50)
    especialidad: str = Field(min_length=1, max_length=100)


class UsuarioSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: str
    rol: str


class Credenciales(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CitaNueva(BaseModel):
    medico_id: int
    fecha: NaiveDatetime


class CitaSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    medico_id: int
    fecha: datetime
    estado: str


class DiagnosticoNuevo(BaseModel):
    descripcion: str = Field(min_length=1)


class DiagnosticoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    descripcion: str
    fecha: date


class ExpedienteSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    diagnosticos: list[DiagnosticoSalida]
