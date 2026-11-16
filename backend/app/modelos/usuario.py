"""Entidades Usuario, Paciente y Medico."""
from datetime import date

import bcrypt
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base_datos import Base


class Usuario(Base):
    """Clase padre de Paciente y Medico. Todos se guardan en la tabla usuarios
    y la columna rol indica de qué clase es cada fila."""

    __tablename__ = "usuarios"
    __mapper_args__ = {"polymorphic_on": "rol"}

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    rol: Mapped[str] = mapped_column(String(20))

    @staticmethod
    def hashear_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def autenticar(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())


class Paciente(Usuario):
    __mapper_args__ = {"polymorphic_identity": "paciente"}

    # Opcional en la tabla porque los médicos comparten la misma tabla
    fecha_nacimiento: Mapped[date | None] = mapped_column(Date)
    expediente: Mapped["Expediente"] = relationship()

    def obtener_edad(self) -> int:
        hoy = date.today()
        ya_cumplio = (hoy.month, hoy.day) >= (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        return hoy.year - self.fecha_nacimiento.year - (0 if ya_cumplio else 1)


class Medico(Usuario):
    __mapper_args__ = {"polymorphic_identity": "medico"}

    matricula: Mapped[str | None] = mapped_column(String(50))
    especialidad: Mapped[str | None] = mapped_column(String(100))
