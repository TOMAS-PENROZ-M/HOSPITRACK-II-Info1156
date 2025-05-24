# recepcionista/management.py

from database import SessionLocal
from models import SolicitudDB

class GestorSolicitudesPrueba:
    """
    Clase encargada de gestionar las solicitudes en un entorno de prueba.
    """
    def __init__(self):
        self.sesion = SessionLocal()

    def obtener_pendientes(self):
        """
        Retorna una lista de solicitudes que están en estado 'pendiente'.
        """
        return self.sesion.query(SolicitudDB).filter_by(estado='pendiente').all()

    def asignar_pruebas(self):
        """
        Asigna automáticamente las solicitudes pendientes con estado 'asignada'.
        Esta es una simulación para efectos de prueba.
        """
        solicitudes = self.obtener_pendientes()
        for solicitud in solicitudes:
            solicitud.estado = 'asignada'
            self.sesion.add(solicitud)

        self.sesion.commit()

    def cerrar_solicitud(self, solicitud_id: int):
        """
        Marca una solicitud como cerrada dado su ID.
        """
        solicitud = self.sesion.query(SolicitudDB).get(solicitud_id)
        if solicitud:
            solicitud.estado = 'cerrada'
            self.sesion.commit()
            return True
        return False

    def eliminar_solicitud(self, solicitud_id: int):
        """
        Elimina una solicitud de la base de datos.
        """
        solicitud = self.sesion.query(SolicitudDB).get(solicitud_id)
        if solicitud:
            self.sesion.delete(solicitud)
            self.sesion.commit()
            return True
        return False
