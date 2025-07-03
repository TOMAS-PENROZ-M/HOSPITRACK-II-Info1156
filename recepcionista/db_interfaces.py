# 1. recepcionista/db_interfaces.py
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

class SolicitudPendiente:
    def __init__(self, id:int, nombre:str, tipo:str, seccion:str, hora_solicitud:datetime, prioridad:str):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.seccion = seccion
        self.hora_solicitud = hora_solicitud
        self.prioridad = prioridad

class AtencionHistorial:
    def __init__(self, id:int, fecha:datetime, seccion:str, tipo:str, comentario:str, estado_final:str, turno_asignado:str):
        self.id = id
        self.fecha = fecha
        self.seccion = seccion
        self.tipo = tipo
        self.comentario = comentario
        self.estado_final = estado_final
        self.turno_asignado = turno_asignado

class IRequestRepository(ABC):
    @abstractmethod
    def get_pending(self, filtros: dict) -> List[SolicitudPendiente]: pass

    @abstractmethod
    def resolve(self, solicitud_id:int, comentario:str, estado:str, turno:str) -> bool: pass

    @abstractmethod
    def get_history(self, filtros: dict) -> List[AtencionHistorial]: pass
