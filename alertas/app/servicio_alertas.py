"""Evaluación de métricas y generación de alertas."""
from app.metrica_salud import MetricaSalud
from app.notificadores import INotificador

DESTINATARIO = "medicos"


class ServicioAlertas:
    def __init__(self, notificadores: list[INotificador], umbral_pulso: float = 120):
        self._notificadores = notificadores
        self._umbral_pulso = umbral_pulso

    async def evaluar_metrica(self, metrica: MetricaSalud) -> None:
        if metrica.tipo != "pulso" or metrica.valor <= self._umbral_pulso:
            return
        mensaje = f"Pulso de {metrica.valor} en el paciente {metrica.paciente_id}"
        for notificador in self._notificadores:
            await notificador.notificar(mensaje, DESTINATARIO)
