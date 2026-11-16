"""Esquemas Pydantic de entrada y salida de la API."""
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, NaiveDatetime, PastDate

FORMATO_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
# MN (nacional) o MP (provincial) seguido de 4 a 6 dígitos, por ejemplo "MN 12345"
FORMATO_MATRICULA = r"^M[NP] ?\d{4,6}$"
Especialidad = Literal[
    "Clínica médica", "Cardiología", "Pediatría", "Traumatología", "Dermatología", "Ginecología"
]


class PacienteNuevo(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=150, pattern=FORMATO_EMAIL)
    password: str = Field(min_length=6, max_length=50)
    fecha_nacimiento: PastDate


class MedicoNuevo(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=150, pattern=FORMATO_EMAIL)
    password: str = Field(min_length=6, max_length=50)
    matricula: str = Field(pattern=FORMATO_MATRICULA)
    especialidad: Especialidad


class UsuarioSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: str
    rol: str


class MedicoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    especialidad: str


class PersonaSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str


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
    paciente: PersonaSalida
    medico: PersonaSalida
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
