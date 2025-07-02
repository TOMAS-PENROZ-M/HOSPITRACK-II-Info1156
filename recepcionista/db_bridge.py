# recepcionista/db_bridge.py

"""
Puente de base de datos para la vista de recepcionista,
trabajando sobre la tabla SolicitudDB y moviendo aceptaciones a EnEsperaDB.
Implementa patrones:
- Singleton (creacional) para única instancia de DBBridge
- Template Method (comportamiento) para acciones aceptar/rechazar
- Facade (estructural) como fachada para operaciones sobre BD
"""

from typing import List
from datetime import datetime
from abc import ABC, abstractmethod
from database import SessionLocal, init_db
from models import SolicitudDB, EnEsperaDB

# ------------------ Singleton ------------------
class SingletonMeta(type):
    """Singleton para asegurar única instancia de DBBridge"""
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# ------------------ Template Method ------------------
class SolicitudProcessor(ABC):
    def __init__(self, session, solicitud: SolicitudDB, comentario: str):
        self.session = session
        self.solicitud = solicitud
        self.comentario = comentario

    def procesar(self) -> bool:
        if not self.solicitud:
            return False

        en_espera = EnEsperaDB(
            RUT=self.solicitud.RUT,
            Prioridad=getattr(self.solicitud, 'Prioridad', 1),
            HoraRegistro=self.solicitud.HoraSolicitud or datetime.utcnow(),
            IdSeccion=getattr(self.solicitud, 'IdSeccion', None),
            Comentario=self.comentario,
            EstadoFinal=self.estado(),
            FechaResolucion=datetime.utcnow()
        )
        self.session.add(en_espera)
        self.session.delete(self.solicitud)
        self.session.commit()
        return True

    @abstractmethod
    def estado(self) -> str:
        pass

class AceptarSolicitud(SolicitudProcessor):
    def estado(self) -> str:
        return "aceptado"

class RechazarSolicitud(SolicitudProcessor):
    def estado(self) -> str:
        return "rechazado"

# ------------------ Facade + Singleton ------------------
class DBBridge(metaclass=SingletonMeta):
    """
    Fachada única para acceder a la base de datos.
    Encapsula operaciones CRUD sobre SolicitudDB y EnEsperaDB.
    """
    def __init__(self):
        init_db()
        self._session = SessionLocal()

    def listar_solicitudes(self) -> List[SolicitudDB]:
        return (
            self._session
                .query(SolicitudDB)
                .order_by(SolicitudDB.HoraSolicitud)
                .all()
        )

    def aceptar_solicitud(self, solicitud_id: int, comentario: str = "") -> bool:
        solicitud = self._session.query(SolicitudDB).get(solicitud_id)
        return AceptarSolicitud(self._session, solicitud, comentario).procesar()

    def rechazar_solicitud(self, solicitud_id: int, comentario: str = "") -> bool:
        solicitud = self._session.query(SolicitudDB).get(solicitud_id)
        return RechazarSolicitud(self._session, solicitud, comentario).procesar()

    def obtener_historial(self) -> List[EnEsperaDB]:
        return (
            self._session.query(EnEsperaDB)
            .filter(EnEsperaDB.EstadoFinal.in_(["aceptado", "rechazado"]))
            .order_by(EnEsperaDB.FechaResolucion.desc())
            .all()
        )

    def cerrar(self) -> None:
        self._session.close()
