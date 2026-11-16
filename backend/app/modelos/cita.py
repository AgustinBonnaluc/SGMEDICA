"""Entidad Cita."""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base_datos import Base
from app.excepciones import ReglaDeNegocioError


class Cita(Base):
    __tablename__ = "citas"

    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"

    id: Mapped[int] = mapped_column(primary_key=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    medico_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    fecha: Mapped[datetime] = mapped_column(DateTime)
    estado: Mapped[str] = mapped_column(String(20))

    def __init__(self, paciente_id: int, medico_id: int, fecha: datetime):
        # Toda cita nace pendiente
        super().__init__(
            paciente_id=paciente_id, medico_id=medico_id, fecha=fecha, estado=self.PENDIENTE
        )

    def confirmar(self) -> None:
        if self.estado != self.PENDIENTE:
            raise ReglaDeNegocioError(f"No se puede confirmar una cita {self.estado}")
        self.estado = self.CONFIRMADA

    def cancelar(self) -> None:
        if self.estado == self.CANCELADA:
            raise ReglaDeNegocioError("La cita ya está cancelada")
        self.estado = self.CANCELADA
