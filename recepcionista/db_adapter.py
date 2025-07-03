# recepcionista/db_adapter.py

from recepcionista.db_interfaces import IRequestRepository, SolicitudPendiente, AtencionHistorial
from recepcionista.db_bridge import DBBridge

class DBBridgeAdapter(IRequestRepository):
    """
    Adaptador que conecta DBBridge con la interfaz IRequestRepository.
    Traduce los modelos SQLAlchemy a los DTOs definidos en db_interfaces.
    """
    def __init__(self):
        self._bridge = DBBridge()

    def get_pending(self, filtros: dict):
        """
        Retorna una lista de SolicitudPendiente para solicitudes en espera.
        Ignora filtros si no se implementan en DBBridge.
        """
        filas = self._bridge.listar_solicitudes()
        resultado = []
        for s in filas:
            dto = SolicitudPendiente(
                id=s.IdSolicitud,
                nombre=f"{s.usuario.Nombre} {s.usuario.Apellido}",
                tipo=s.Mensaje,
                seccion=s.seccion.NombreSeccion,
                hora_solicitud=s.HoraSolicitud,
                prioridad=getattr(s, 'Prioridad', 'Normal')
            )
            resultado.append(dto)
        return resultado

    def resolve(self, solicitud_id: int, comentario: str, estado: str, turno: str) -> bool:
        """
        Procesa la resolución de una solicitud, aceptándola o rechazándola.
        """
        if estado == 'aceptado':
            return self._bridge.aceptar_solicitud(solicitud_id, comentario, turno)
        else:
            return self._bridge.rechazar_solicitud(solicitud_id, comentario)

    def get_history(self, filtros: dict):
        """
        Retorna una lista de AtencionHistorial con el historial de atenciones.
        Ignora filtros si no se implementan en DBBridge.
        """
        filas = self._bridge.obtener_historial()
        resultado = []
        for r in filas:
            dto = AtencionHistorial(
                id=r.IdRegistro,
                fecha=r.FechaResolucion,
                seccion=r.seccion.NombreSeccion,
                tipo=r.Prioridad,
                comentario=r.Comentario,
                estado_final=r.EstadoFinal,
                turno_asignado=getattr(r, 'TurnoAsignado', '')
            )
            resultado.append(dto)
        return resultado