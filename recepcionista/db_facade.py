# recepcionista/db_facade.py
"""
Facade para operaciones CRUD de SolicitudDB usando la base de datos local.
"""
from typing import List
from database import SessionLocal
from models import SolicitudDB  # Importa la entidad ORM del módulo raíz

class DBRecepcionistaFacade:
    """
    Facade que conecta con la base de datos y expone métodos para:
    - listar solicitudes pendientes
    - aceptar solicitudes
    - rechazar solicitudes
    - cerrar la sesión
    """
    def __init__(self):
        self._session = SessionLocal()

    def listar_solicitudes(self) -> List[SolicitudDB]:
        """Retorna todas las solicitudes cuyo estado sea 'pendiente'."""
        return (
            self._session
                .query(SolicitudDB)
                .filter(SolicitudDB.estado == 'pendiente')
                .order_by(SolicitudDB.id)
                .all()
        )

    def aceptar_solicitud(self, solicitud_id: int) -> bool:
        """
        Cambia el estado de la solicitud a 'aceptada'.
        Retorna True si la solicitud existía y se actualizó, False si no.
        """
        solicitud = self._session.query(SolicitudDB).get(solicitud_id)
        if solicitud is None:
            return False
        solicitud.estado = 'aceptada'
        self._session.commit()
        return True

    def rechazar_solicitud(self, solicitud_id: int) -> bool:
        """
        Cambia el estado de la solicitud a 'rechazada'.
        Retorna True si la solicitud existía y se actualizó, False si no.
        """
        solicitud = self._session.query(SolicitudDB).get(solicitud_id)
        if solicitud is None:
            return False
        solicitud.estado = 'rechazada'
        self._session.commit()
        return True

    def close(self) -> None:
        """Cierra la sesión de base de datos."""
        self._session.close()
