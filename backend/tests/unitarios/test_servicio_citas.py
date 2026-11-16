"""Pruebas unitarias de ServicioCitas."""
from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from app.excepciones import NoEncontradoError, ReglaDeNegocioError
from app.modelos import Cita, Medico
from app.repositorios.interfaces import IRepositorioCitas, IRepositorioUsuarios
from app.servicios.servicio_citas import ServicioCitas

PACIENTE_ID = 1
MEDICO_ID = 2
FECHA_FUTURA = datetime.now() + timedelta(days=1)


@pytest.fixture
def repositorio():
    repositorio = Mock(spec=IRepositorioCitas)
    repositorio.guardar.side_effect = lambda cita: cita
    repositorio.listar_por_medico.return_value = []
    return repositorio


@pytest.fixture
def repositorio_usuarios():
    repositorio_usuarios = Mock(spec=IRepositorioUsuarios)
    repositorio_usuarios.buscar_por_id.return_value = Medico(id=MEDICO_ID)
    return repositorio_usuarios


@pytest.fixture
def servicio(repositorio, repositorio_usuarios):
    # Se inyectan repositorios falsos: el test no necesita base de datos
    return ServicioCitas(repositorio, repositorio_usuarios)


def test_agendar_guarda_una_cita_pendiente(servicio, repositorio):
    cita = servicio.agendar_cita(PACIENTE_ID, MEDICO_ID, FECHA_FUTURA)

    assert cita.estado == Cita.PENDIENTE
    repositorio.guardar.assert_called_once_with(cita)


def test_agendar_rechaza_una_fecha_pasada(servicio, repositorio):
    ayer = datetime.now() - timedelta(days=1)

    with pytest.raises(ReglaDeNegocioError):
        servicio.agendar_cita(PACIENTE_ID, MEDICO_ID, ayer)

    repositorio.guardar.assert_not_called()


def test_agendar_rechaza_un_medico_inexistente(servicio, repositorio, repositorio_usuarios):
    repositorio_usuarios.buscar_por_id.return_value = None

    with pytest.raises(NoEncontradoError):
        servicio.agendar_cita(PACIENTE_ID, MEDICO_ID, FECHA_FUTURA)

    repositorio.guardar.assert_not_called()


def test_agendar_rechaza_un_horario_ocupado(servicio, repositorio):
    repositorio.listar_por_medico.return_value = [Cita(99, MEDICO_ID, FECHA_FUTURA)]
    diez_minutos_despues = FECHA_FUTURA + timedelta(minutes=10)

    with pytest.raises(ReglaDeNegocioError):
        servicio.agendar_cita(PACIENTE_ID, MEDICO_ID, diez_minutos_despues)

    repositorio.guardar.assert_not_called()


def test_agendar_permite_el_turno_siguiente(servicio, repositorio):
    repositorio.listar_por_medico.return_value = [Cita(99, MEDICO_ID, FECHA_FUTURA)]

    cita = servicio.agendar_cita(PACIENTE_ID, MEDICO_ID, FECHA_FUTURA + Cita.DURACION)

    assert cita.estado == Cita.PENDIENTE


def test_agendar_permite_el_horario_de_una_cita_cancelada(servicio, repositorio):
    cancelada = Cita(99, MEDICO_ID, FECHA_FUTURA)
    cancelada.cancelar()
    repositorio.listar_por_medico.return_value = [cancelada]

    cita = servicio.agendar_cita(PACIENTE_ID, MEDICO_ID, FECHA_FUTURA)

    assert cita.estado == Cita.PENDIENTE


def test_confirmar_cambia_el_estado_a_confirmada(servicio, repositorio):
    repositorio.buscar_por_id.return_value = Cita(PACIENTE_ID, MEDICO_ID, FECHA_FUTURA)

    cita = servicio.confirmar_cita(cita_id=10, usuario_id=MEDICO_ID)

    assert cita.estado == Cita.CONFIRMADA


def test_cancelar_cambia_el_estado_a_cancelada(servicio, repositorio):
    repositorio.buscar_por_id.return_value = Cita(PACIENTE_ID, MEDICO_ID, FECHA_FUTURA)

    cita = servicio.cancelar_cita(cita_id=10, usuario_id=PACIENTE_ID)

    assert cita.estado == Cita.CANCELADA


def test_cancelar_rechaza_a_un_usuario_ajeno_a_la_cita(servicio, repositorio):
    repositorio.buscar_por_id.return_value = Cita(PACIENTE_ID, MEDICO_ID, FECHA_FUTURA)

    with pytest.raises(NoEncontradoError):
        servicio.cancelar_cita(cita_id=10, usuario_id=99)

    repositorio.guardar.assert_not_called()
