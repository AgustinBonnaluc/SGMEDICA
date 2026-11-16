"""Lógica de negocio de autenticación."""
from datetime import date, datetime, timedelta, timezone

import jwt

from app.config import JWT_ALGORITMO, JWT_MINUTOS_DE_VIDA, JWT_SECRETO
from app.excepciones import CredencialesInvalidasError, ReglaDeNegocioError
from app.modelos import Expediente, Medico, Paciente, Usuario
from app.repositorios.interfaces import IRepositorioUsuarios


class ServicioAuth:
    def __init__(self, repositorio: IRepositorioUsuarios):
        self._repositorio = repositorio

    def registrar_paciente(
        self, nombre: str, email: str, password: str, fecha_nacimiento: date
    ) -> Paciente:
        self._validar_email_libre(email)
        paciente = Paciente(
            nombre=nombre,
            email=email,
            password_hash=Usuario.hashear_password(password),
            fecha_nacimiento=fecha_nacimiento,
            expediente=Expediente(),
        )
        return self._repositorio.guardar(paciente)

    def registrar_medico(
        self, nombre: str, email: str, password: str, matricula: str, especialidad: str
    ) -> Medico:
        self._validar_email_libre(email)
        medico = Medico(
            nombre=nombre,
            email=email,
            password_hash=Usuario.hashear_password(password),
            matricula=matricula,
            especialidad=especialidad,
        )
        return self._repositorio.guardar(medico)

    def login(self, email: str, password: str) -> str:
        """Devuelve un token JWT si las credenciales son correctas."""
        usuario = self._repositorio.buscar_por_email(email)
        if usuario is None or not usuario.autenticar(password):
            raise CredencialesInvalidasError("Email o contraseña incorrectos")
        vencimiento = datetime.now(timezone.utc) + timedelta(minutes=JWT_MINUTOS_DE_VIDA)
        datos = {"sub": str(usuario.id), "exp": vencimiento}
        return jwt.encode(datos, JWT_SECRETO, algorithm=JWT_ALGORITMO)

    def usuario_desde_token(self, token: str) -> Usuario:
        try:
            datos = jwt.decode(token, JWT_SECRETO, algorithms=[JWT_ALGORITMO])
        except jwt.InvalidTokenError:
            raise CredencialesInvalidasError("Token inválido o vencido")
        usuario = self._repositorio.buscar_por_id(int(datos["sub"]))
        if usuario is None:
            raise CredencialesInvalidasError("Token inválido o vencido")
        return usuario

    def listar_medicos(self) -> list[Medico]:
        return self._repositorio.listar_medicos()

    def _validar_email_libre(self, email: str) -> None:
        if self._repositorio.buscar_por_email(email) is not None:
            raise ReglaDeNegocioError("Ya existe un usuario con ese email")
