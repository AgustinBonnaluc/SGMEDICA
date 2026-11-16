"""Métrica de salud recibida desde Redis."""
import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetricaSalud:
    paciente_id: int
    tipo: str
    valor: float
    timestamp: datetime

    @classmethod
    def desde_json(cls, texto: str) -> "MetricaSalud":
        datos = json.loads(texto)
        return cls(
            paciente_id=int(datos["paciente_id"]),
            tipo=datos["tipo"],
            valor=float(datos["valor"]),
            timestamp=datetime.fromisoformat(datos["timestamp"]),
        )
