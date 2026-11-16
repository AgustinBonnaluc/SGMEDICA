"""Suscripción al canal de métricas en Redis."""
import logging

from redis.asyncio import Redis

from app.metrica_salud import MetricaSalud
from app.servicio_alertas import ServicioAlertas

CANAL_METRICAS = "metricas_salud"

logger = logging.getLogger(__name__)


async def escuchar_metricas(redis_url: str, servicio: ServicioAlertas) -> None:
    redis = Redis.from_url(redis_url, decode_responses=True)
    async with redis.pubsub() as canal:
        await canal.subscribe(CANAL_METRICAS)
        async for mensaje in canal.listen():
            if mensaje["type"] != "message":
                continue
            try:
                await servicio.evaluar_metrica(MetricaSalud.desde_json(mensaje["data"]))
            except Exception:
                # Una métrica mal formada no debe cortar la escucha
                logger.exception("No se pudo procesar la métrica: %s", mensaje["data"])
