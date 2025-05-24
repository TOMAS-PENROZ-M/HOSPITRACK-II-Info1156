# recepcionista/management.py

import logging
import threading
import time
from datetime import datetime, timedelta
from typing import List, Dict

from sqlalchemy.orm import Session
from database import SessionLocal
from models import SolicitudDB, UsuarioDB

logger = logging.getLogger("recepcionista.management")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class SolicitudManagerTest:
    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()
        self.lock = threading.Lock()
        self.last_summary: Dict[str, int] = {}

    def obtener_pendientes(self) -> List[SolicitudDB]:
        pendientes = self.session.query(SolicitudDB).filter_by(estado="pendiente").all()
        logger.debug(f"Obtenidas {len(pendientes)} solicitudes pendientes")
        return pendientes

    def asignar_pruebas(self) -> None:
        with self.lock:
            pendientes = self.obtener_pendientes()
            for solicitud in pendientes:
                solicitud.estado = "en_proceso"
                solicitud.asignado_a = "Recepcionista-Test"
                solicitud.fecha_asignacion = datetime.utcnow()
                self.session.add(solicitud)
            self.session.commit()
            logger.info(f"Asignadas {len(pendientes)} solicitudes a Recepcionista-Test")

    def procesar_solicitud(self, solicitud_id: int, nuevo_estado: str) -> bool:
        solicitud = self.session.query(SolicitudDB).get(solicitud_id)
        if not solicitud:
            logger.error(f"Solicitud con ID {solicitud_id} no encontrada")
            return False
        if solicitud.estado == "cerrada":
            logger.warning(f"Solicitud {solicitud_id} ya está cerrada")
            return False
        solicitud.estado = nuevo_estado
        solicitud.fecha_modificacion = datetime.utcnow()
        self.session.add(solicitud)
        self.session.commit()
        logger.info(f"Solicitud {solicitud_id} procesada a estado {nuevo_estado}")
        return True

    def reasignar(self, solicitud_id: int, usuario_username: str) -> bool:
        solicitud = self.session.query(SolicitudDB).get(solicitud_id)
        usuario = self.session.query(UsuarioDB).filter_by(username=usuario_username).first()
        if not solicitud or not usuario:
            logger.error("Solicitud o usuario no encontrados para reasignar")
            return False
        solicitud.asignado_a = usuario_username
        solicitud.fecha_modificacion = datetime.utcnow()
        self.session.add(solicitud)
        self.session.commit()
        logger.info(f"Solicitud {solicitud_id} reasignada a {usuario_username}")
        return True

    def cerrar_solicitud(self, solicitud_id: int) -> bool:
        return self.procesar_solicitud(solicitud_id, "cerrada")

    def resumen_estadisticas(self) -> Dict[str, int]:
        total = self.session.query(SolicitudDB).count()
        pendientes = self.session.query(SolicitudDB).filter_by(estado="pendiente").count()
        en_proceso = self.session.query(SolicitudDB).filter_by(estado="en_proceso").count()
        cerradas = self.session.query(SolicitudDB).filter_by(estado="cerrada").count()
        resumen = {
            "total": total,
            "pendientes": pendientes,
            "en_proceso": en_proceso,
            "cerradas": cerradas,
        }
        logger.debug(f"Resumen de estado: {resumen}")
        return resumen

    def ejecutar_prueba_periodica(self, interval_sec: int = 60, stop_after: int = 300):
        start_time = time.time()
        logger.info("Inicio de pruebas periódicas de gestión de solicitudes")
        while time.time() - start_time < stop_after:
            try:
                self.asignar_pruebas()
                summary = self.resumen_estadisticas()
                if summary != self.last_summary:
                    logger.info(f"Nueva estadística: {summary}")
                    self.last_summary = summary
                time.sleep(interval_sec)
            except Exception as e:
                logger.exception(f"Error durante ejecución periódica: {e}")
                break
        logger.info("Fin de pruebas periódicas de gestión de solicitudes")

if __name__ == "__main__":
    manager = SolicitudManagerTest()
    print("Solicitudes pendientes iniciales:", len(manager.obtener_pendientes()))
    manager.asignar_pruebas()
    print("Resumen después de asignar:", manager.resumen_estadisticas())
    # Ejecuta pruebas periódicas en un hilo
    thread = threading.Thread(target=manager.ejecutar_prueba_periodica, kwargs={"interval_sec": 30, "stop_after": 120})
    thread.start()
    thread.join()
