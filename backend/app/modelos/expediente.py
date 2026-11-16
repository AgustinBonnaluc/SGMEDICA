"""Entidades Expediente y Diagnostico."""
from datetime import date

from sqlalchemy import Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base_datos import Base


class Expediente(Base):
    __tablename__ = "expedientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    # unique: cada paciente tiene un solo expediente
    paciente_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), unique=True)
    diagnosticos: Mapped[list["Diagnostico"]] = relationship(order_by="Diagnostico.fecha")

    def agregar_diagnostico(self, diagnostico: "Diagnostico") -> None:
        self.diagnosticos.append(diagnostico)


class Diagnostico(Base):
    __tablename__ = "diagnosticos"

    id: Mapped[int] = mapped_column(primary_key=True)
    expediente_id: Mapped[int] = mapped_column(ForeignKey("expedientes.id"))
    descripcion: Mapped[str] = mapped_column(Text)
    fecha: Mapped[date] = mapped_column(Date)
