"""Entidad MetricaSalud."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetricaSalud:
    """Se guarda en MongoDB, por eso no usa SQLAlchemy."""

    paciente_id: int
    tipo: str  # pulso, presion_sistolica o presion_diastolica
    valor: float
    timestamp: datetime
