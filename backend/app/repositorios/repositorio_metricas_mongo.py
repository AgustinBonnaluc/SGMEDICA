"""Acceso a métricas de salud en MongoDB."""
from pymongo.collection import Collection

from app.modelos import MetricaSalud
from app.repositorios.interfaces import IRepositorioMetricas


class RepositorioMetricasMongo(IRepositorioMetricas):
    def __init__(self, coleccion: Collection):
        self._coleccion = coleccion

    def listar_por_paciente(self, paciente_id: int, limite: int) -> list[MetricaSalud]:
        """Devuelve las métricas más recientes primero."""
        documentos = (
            self._coleccion.find({"paciente_id": paciente_id}).sort("timestamp", -1).limit(limite)
        )
        return [
            MetricaSalud(d["paciente_id"], d["tipo"], d["valor"], d["timestamp"]) for d in documentos
        ]
