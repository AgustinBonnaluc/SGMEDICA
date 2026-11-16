"""Interfaz INotificador y sus implementaciones."""
import logging
from abc import ABC, abstractmethod

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class INotificador(ABC):
    @abstractmethod
    async def notificar(self, mensaje: str, destinatario: str) -> None: ...


class NotificadorLog(INotificador):
    async def notificar(self, mensaje: str, destinatario: str) -> None:
        logger.warning("Alerta para %s: %s", destinatario, mensaje)


class NotificadorWebSocket(INotificador):
    """Envía la alerta a todos los clientes conectados."""

    def __init__(self):
        self._conexiones: set[WebSocket] = set()

    async def conectar(self, conexion: WebSocket) -> None:
        await conexion.accept()
        self._conexiones.add(conexion)

    def desconectar(self, conexion: WebSocket) -> None:
        self._conexiones.discard(conexion)

    async def notificar(self, mensaje: str, destinatario: str) -> None:
        for conexion in list(self._conexiones):
            await conexion.send_json({"destinatario": destinatario, "mensaje": mensaje})
