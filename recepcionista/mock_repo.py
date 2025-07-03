# mock_repo.py
from recepcionista.db_interfaces import IRequestRepository, SolicitudPendiente, AtencionHistorial
from datetime import datetime

class MockRepo(IRequestRepository):
    def get_pending(self, filtros):
        return [
            SolicitudPendiente(1, "Ana Soto", "Consulta", "Medicina", datetime.now(), "alta"),
            SolicitudPendiente(2, "Luis Vega", "Examen", "Radiología", datetime.now(), "media")
        ]
    def get_history(self, filtros):
        return [
            AtencionHistorial(1, datetime.now(), "Medicina", "Consulta", "Todo ok", "aceptado", "Mañana"),
            AtencionHistorial(2, datetime.now(), "Radiología", "Examen", "Cancelado", "rechazado", "Tarde")
        ]
    def resolve(self, solicitud_id, comentario, estado, turno):
        print(f"[Mock] Resolviendo ID {solicitud_id} como {estado} con turno {turno}. Comentario: {comentario}")
        return True
