# recepcionista/db_bridge.py

"""
Puente de base de datos para la vista de recepcionista,
trabajando sobre la tabla SolicitudDB y moviendo aceptaciones a EnEsperaDB.
"""

from typing import List
from datetime import datetime
from database import SessionLocal, init_db
from models import SolicitudDB, EnEsperaDB

class DBBridge:
    """
    Maneja:
      - listar solicitudes pendientes
      - aceptar: mover solicitud a la fila de espera (EnEsperaDB)
      - rechazar: eliminar solicitud
      - cerrar sesión
    """
    def __init__(self):
        init_db()  # asegúrate de que las tablas existan
        self._session = SessionLocal()

    def listar_solicitudes(self) -> List[SolicitudDB]:
        """
        Retorna todas las solicitudes con estado 'pendiente'.
        """
        return (
            self._session
                .query(SolicitudDB)
                .order_by(SolicitudDB.HoraSolicitud)
                .all()
        )

    def aceptar_solicitud(self, solicitud_id: int) -> bool:
        """
        Mueve la solicitud de SolicitudDB a EnEsperaDB:
        - Crea un registro en EnEsperaDB
        - Elimina la solicitud original
        Retorna True si tuvo éxito.
        """
        solicitud = self._session.query(SolicitudDB).get(solicitud_id)
        if solicitud is None:
            return False

        # Crear nueva entrada en EnEsperaDB copiando campos relevantes
        espera = EnEsperaDB(
            RUT=solicitud.RUT,
            Prioridad=getattr(solicitud, 'Prioridad', 1),
            HoraRegistro=solicitud.HoraSolicitud or datetime.utcnow(),
            IdSeccion=getattr(solicitud, 'IdSeccion', None)
        )
        self._session.add(espera)
        # Eliminar la solicitud original
        self._session.delete(solicitud)
        self._session.commit()
        return True

    def rechazar_solicitud(self, solicitud_id: int) -> bool:
        """
        Elimina la solicitud de SolicitudDB.
        Retorna True si existía y fue borrada.
        """
        solicitud = self._session.query(SolicitudDB).get(solicitud_id)
        if solicitud is None:
            return False
        self._session.delete(solicitud)
        self._session.commit()
        return True

    def cerrar(self) -> None:
        """
        Cierra la sesión de base de datos.
        """
        self._session.close()
