"""Punto de entrada del microservicio: WebSocket y suscriptor de Redis."""
import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.notificadores import NotificadorLog, NotificadorWebSocket
from app.servicio_alertas import ServicioAlertas
from app.suscriptor_redis import escuchar_metricas

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

logging.basicConfig(level=logging.INFO)

# Inyección de dependencias: el servicio solo conoce la interfaz INotificador
notificador_websocket = NotificadorWebSocket()
servicio = ServicioAlertas([NotificadorLog(), notificador_websocket])


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    tarea = asyncio.create_task(escuchar_metricas(REDIS_URL, servicio))
    yield
    tarea.cancel()


app = FastAPI(title="SGMEDICA Alertas", lifespan=ciclo_de_vida)


@app.websocket("/ws/alertas")
async def recibir_alertas(conexion: WebSocket):
    await notificador_websocket.conectar(conexion)
    try:
        while True:
            await conexion.receive_text()
    except WebSocketDisconnect:
        notificador_websocket.desconectar(conexion)
