"""Pruebas unitarias de ServicioAlertas."""
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.metrica_salud import MetricaSalud
from app.notificadores import INotificador
from app.servicio_alertas import ServicioAlertas

UMBRAL_PULSO = 120


@pytest.fixture
def notificador():
    return AsyncMock(spec=INotificador)


@pytest.fixture
def servicio(notificador):
    # Se inyecta un notificador falso: el test no necesita Redis ni WebSocket
    return ServicioAlertas([notificador], umbral_pulso=UMBRAL_PULSO)


def evaluar(servicio: ServicioAlertas, tipo: str, valor: float) -> None:
    metrica = MetricaSalud(paciente_id=1, tipo=tipo, valor=valor, timestamp=datetime.now())
    asyncio.run(servicio.evaluar_metrica(metrica))


def test_notifica_cuando_el_pulso_supera_el_umbral(servicio, notificador):
    evaluar(servicio, "pulso", 130)

    notificador.notificar.assert_awaited_once_with("Pulso de 130 en el paciente 1", "medicos")


def test_no_notifica_cuando_el_pulso_es_normal(servicio, notificador):
    evaluar(servicio, "pulso", 80)

    notificador.notificar.assert_not_awaited()


def test_no_notifica_cuando_el_pulso_es_igual_al_umbral(servicio, notificador):
    evaluar(servicio, "pulso", UMBRAL_PULSO)

    notificador.notificar.assert_not_awaited()


def test_no_notifica_por_otros_tipos_de_metrica(servicio, notificador):
    evaluar(servicio, "presion_sistolica", 150)

    notificador.notificar.assert_not_awaited()


def test_notifica_a_todos_los_notificadores():
    primero, segundo = AsyncMock(spec=INotificador), AsyncMock(spec=INotificador)
    servicio = ServicioAlertas([primero, segundo], umbral_pulso=UMBRAL_PULSO)

    evaluar(servicio, "pulso", 130)

    primero.notificar.assert_awaited_once()
    segundo.notificar.assert_awaited_once()
