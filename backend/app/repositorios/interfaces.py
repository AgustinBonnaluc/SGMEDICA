"""Interfaces de los repositorios."""
from abc import ABC, abstractmethod

from app.modelos import Cita, Expediente, MetricaSalud, Usuario


class IRepositorioUsuarios(ABC):
    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario: ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Usuario | None: ...

    @abstractmethod
    def buscar_por_email(self, email: str) -> Usuario | None: ...


class IRepositorioCitas(ABC):
    @abstractmethod
    def guardar(self, cita: Cita) -> Cita: ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Cita | None: ...

    @abstractmethod
    def listar_por_paciente(self, paciente_id: int) -> list[Cita]: ...


class IRepositorioExpedientes(ABC):
    @abstractmethod
    def guardar(self, expediente: Expediente) -> Expediente: ...

    @abstractmethod
    def buscar_por_paciente(self, paciente_id: int) -> Expediente | None: ...


class IRepositorioMetricas(ABC):
    @abstractmethod
    def listar_por_paciente(self, paciente_id: int, limite: int) -> list[MetricaSalud]: ...
