# recepcionista/models_recep.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, List, Any
from enum import Enum
from threading import Lock

# ------------------------------------------------------------------------
# PATRÓN STATE para gestionar estados de Solicitud
# ------------------------------------------------------------------------

class EstadoSolicitud(Protocol):
    def procesar(self, solicitud: 'Solicitud', **kwargs) -> None:
        ...

class PendienteState:
    def procesar(self, solicitud: 'Solicitud', **kwargs) -> None:
        solicitud._estado = 'pendiente'

class AsignadaState:
    def procesar(self, solicitud: 'Solicitud', usuario: str, **kwargs) -> None:
        solicitud._estado = 'asignada'
        solicitud.asignado_a = usuario
        solicitud.fecha_asignacion = datetime.utcnow()

class CerradaState:
    def procesar(self, solicitud: 'Solicitud', **kwargs) -> None:
        solicitud._estado = 'cerrada'
        solicitud.fecha_cierre = datetime.utcnow()

# ------------------------------------------------------------------------
# ENTIDAD Solicitud
# ------------------------------------------------------------------------

@dataclass
class Solicitud:
    titulo: str
    descripcion: str
    es_urgente: bool = False
    id: int = field(init=False)
    _estado: str = field(init=False, default='pendiente')
    fecha_creacion: datetime = field(init=False, default_factory=datetime.utcnow)
    asignado_a: str = field(init=False, default='')
    fecha_asignacion: datetime = field(init=False, default=None)
    fecha_cierre: datetime = field(init=False, default=None)
    _state: EstadoSolicitud = field(init=False, default_factory=PendienteState)

    def __post_init__(self):
        # El ID real se asigna desde el factory
        self.id = 0

    def cambiar_estado(self, state: EstadoSolicitud, **kwargs) -> None:
        state.procesar(self, **kwargs)
        self._state = state

    @property
    def estado(self) -> str:
        return self._estado

# ------------------------------------------------------------------------
# FACTORY METHOD para crear Solicitudes
# ------------------------------------------------------------------------

class SolicitudFactory:
    _next_id: int = 1

    @classmethod
    def crear_solicitud_normal(cls, titulo: str, descripcion: str) -> Solicitud:
        solicitud = Solicitud(titulo=titulo, descripcion=descripcion)
        solicitud.id = cls._next_id
        cls._next_id += 1
        return solicitud

    @classmethod
    def crear_solicitud_urgente(cls, titulo: str, descripcion: str) -> Solicitud:
        solicitud = Solicitud(titulo=titulo, descripcion=descripcion, es_urgente=True)
        solicitud.id = cls._next_id
        cls._next_id += 1
        return solicitud

# ------------------------------------------------------------------------
# REPOSITORIO IN-MEMORIA + OBSERVER
# ------------------------------------------------------------------------

class Observador(Protocol):
    def actualizar(self, evento: str, datos: Any) -> None:
        ...

class SolicitudRepository:
    """
    Singleton en memoria que almacena Solicitud y notifica observadores.
    """
    _instance: 'SolicitudRepository' = None
    _lock: Lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._inicializar()
        return cls._instance

    def _inicializar(self):
        self._solicitudes: List[Solicitud] = []
        self._observadores: List[Observador] = []

    def agregar(self, solicitud: Solicitud) -> None:
        self._solicitudes.append(solicitud)
        self._notificar('agregar', solicitud)

    def listar(self) -> List[Solicitud]:
        return list(self._solicitudes)

    def registrar_observador(self, obs: Observador) -> None:
        self._observadores.append(obs)

    def _notificar(self, evento: str, datos: Any) -> None:
        for obs in self._observadores:
            obs.actualizar(evento, datos)

# ------------------------------------------------------------------------
# PATRÓN COMMAND para operaciones sobre Solicitud
# ------------------------------------------------------------------------

class Command(Protocol):
    def ejecutar(self) -> Any:
        ...

class AgregarSolicitudCommand:
    def __init__(self, repo: SolicitudRepository, solicitud: Solicitud):
        self.repo = repo
        self.solicitud = solicitud

    def ejecutar(self) -> None:
        self.repo.agregar(self.solicitud)

class AsignarPendientesCommand:
    def __init__(self, repo: SolicitudRepository, usuario: str):
        self.repo = repo
        self.usuario = usuario

    def ejecutar(self) -> None:
        pendientes = [s for s in self.repo.listar() if s.estado == 'pendiente']
        for s in pendientes:
            s.cambiar_estado(AsignadaState(), usuario=self.usuario)
            self.repo._notificar('cambiar_estado', s)

class CerrarSolicitudCommand:
    def __init__(self, repo: SolicitudRepository, solicitud_id: int):
        self.repo = repo
        self.solicitud_id = solicitud_id

    def ejecutar(self) -> bool:
        for s in self.repo.listar():
            if s.id == self.solicitud_id:
                s.cambiar_estado(CerradaState())
                self.repo._notificar('cambiar_estado', s)
                return True
        return False

# ------------------------------------------------------------------------
# FACADE para simplificar la API a la vista
# ------------------------------------------------------------------------

class RecepcionistaFacade:
    """
    Proporciona métodos para la UI, ocultando la complejidad interna.
    """
    def __init__(self):
        self.repo = SolicitudRepository()

    def obtener_solicitudes(self) -> List[Solicitud]:
        return self.repo.listar()

    def agregar_solicitud(self, solicitud: Solicitud) -> None:
        AgregarSolicitudCommand(self.repo, solicitud).ejecutar()

    def asignar_pendientes(self, usuario: str = 'Recepcionista') -> None:
        AsignarPendientesCommand(self.repo, usuario).ejecutar()

    def cerrar_solicitud(self, solicitud_id: int) -> bool:
        return CerrarSolicitudCommand(self.repo, solicitud_id).ejecutar()
