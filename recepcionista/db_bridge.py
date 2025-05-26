# recepcionista/db_bridge.py
"""
Módulo puente para compartir la misma sesión y modelos que usa app.py,
permitiendo a views.py conectarse a la base de datos central.
"""
from database import SessionLocal, engine, Base
import models as root_models  # Importa el módulo de modelos raíz
from sqlalchemy.orm import Session

# Inicializa esquemas si no existen
Base.metadata.create_all(bind=engine)

class DBBridge:
    """
    Clase que expone una sesión compartida y métodos básicos para interactuar
    con las tablas de SolicitudDB y UsuarioDB definidas en app.py.
    """
    def __init__(self):
        self.session: Session = SessionLocal()
        # Determina dinámicamente el modelo SolicitudDB y sus columnas
        self.SolicitudModel = root_models.SolicitudDB
        # Identificador de estado y pk
        self.status_attr = 'Estado' if hasattr(self.SolicitudModel, 'Estado') else 'estado'
        pk_name = self.SolicitudModel.__mapper__.primary_key[0].name
        self.pk_attr = pk_name

    def obtener_solicitudes_pendientes(self):
        """
        Retorna todas las solicitudes con estado 'pendiente'.
        """
        status_col = getattr(self.SolicitudModel, self.status_attr)
        pk_col = getattr(self.SolicitudModel, self.pk_attr)
        return (
            self.session
                .query(self.SolicitudModel)
                .filter(status_col == 'pendiente')
                .order_by(pk_col)
                .all()
        )

    def aceptar_solicitud(self, solicitud_id: int) -> bool:
        sol = self.session.query(self.SolicitudModel).get(solicitud_id)
        if not sol:
            return False
        setattr(sol, self.status_attr, 'aceptada')
        self.session.commit()
        return True

    def rechazar_solicitud(self, solicitud_id: int) -> bool:
        sol = self.session.query(self.SolicitudModel).get(solicitud_id)
        if not sol:
            return False
        setattr(sol, self.status_attr, 'rechazada')
        self.session.commit()
        return True

    def cerrar(self):
        """
        Cierra la sesión de base de datos.
        """
        self.session.close()
