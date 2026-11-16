"""Lógica de negocio de citas."""
from datetime import datetime

from app.excepciones import NoEncontradoError, ReglaDeNegocioError
from app.modelos import Cita, Medico, Usuario
from app.repositorios.interfaces import IRepositorioCitas, IRepositorioUsuarios


class ServicioCitas:
    def __init__(self, repositorio: IRepositorioCitas, repositorio_usuarios: IRepositorioUsuarios):
        self._repositorio = repositorio
        self._repositorio_usuarios = repositorio_usuarios

    def agendar_cita(self, paciente_id: int, medico_id: int, fecha: datetime) -> Cita:
        if fecha <= datetime.now():
            raise ReglaDeNegocioError("La fecha de la cita debe ser futura")
        medico = self._repositorio_usuarios.buscar_por_id(medico_id)
        if not isinstance(medico, Medico):
            raise NoEncontradoError("El médico no existe")
        return self._repositorio.guardar(Cita(paciente_id, medico_id, fecha))

    def confirmar_cita(self, cita_id: int, usuario_id: int) -> Cita:
        cita = self._buscar_cita(cita_id, usuario_id)
        cita.confirmar()
        return self._repositorio.guardar(cita)

    def cancelar_cita(self, cita_id: int, usuario_id: int) -> Cita:
        cita = self._buscar_cita(cita_id, usuario_id)
        cita.cancelar()
        return self._repositorio.guardar(cita)

    def listar_citas(self, usuario: Usuario) -> list[Cita]:
        if isinstance(usuario, Medico):
            return self._repositorio.listar_por_medico(usuario.id)
        return self._repositorio.listar_por_paciente(usuario.id)

    def _buscar_cita(self, cita_id: int, usuario_id: int) -> Cita:
        """Devuelve la cita solo si el usuario participa en ella."""
        cita = self._repositorio.buscar_por_id(cita_id)
        if cita is None or usuario_id not in (cita.paciente_id, cita.medico_id):
            raise NoEncontradoError("La cita no existe")
        return cita
