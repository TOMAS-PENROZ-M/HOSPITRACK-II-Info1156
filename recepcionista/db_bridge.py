# 2. recepcionista/db_bridge.py
import os
from datetime import datetime
from typing import List
from sqlalchemy import and_
from database import SessionLocal, init_db
from models import SolicitudDB, EnEsperaDB
from recepcionista.db_interfaces import IRequestRepository, SolicitudPendiente, AtencionHistorial
from recepcionista.patrones.rule_engine import RuleEngine

class DBBridge(IRequestRepository):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'): return
        init_db()
        self._session = SessionLocal()
        self.rule_engine = RuleEngine()
        self._initialized = True

    def get_pending(self, filtros: dict) -> List[SolicitudPendiente]:
        q = self._session.query(SolicitudDB)
        if filtros.get('seccion'):
            q = q.filter(SolicitudDB.IdSeccion == filtros['seccion'])
        if filtros.get('tipo'):
            q = q.filter(SolicitudDB.Tipo == filtros['tipo'])
        raws = q.order_by(SolicitudDB.HoraSolicitud).all()
        return [SolicitudPendiente(r.id, r.Nombre, r.Tipo, r.IdSeccion, r.HoraSolicitud, r.Prioridad) for r in raws]

    def resolve(self, solicitud_id:int, comentario:str, estado:str, turno:str) -> bool:
        sol = self._session.query(SolicitudDB).get(solicitud_id)
        if not sol: return False
        record = EnEsperaDB(
            RUT=sol.RUT,
            Prioridad=sol.Prioridad,
            HoraRegistro=sol.HoraSolicitud,
            IdSeccion=sol.IdSeccion,
            Tipo=sol.Tipo,
            Comentario=comentario,
            EstadoFinal=estado,
            FechaResolucion=datetime.utcnow(),
            TurnoAsignado=turno
        )
        self._session.add(record)
        self._session.delete(sol)
        self._session.commit()
        return True

    def get_history(self, filtros: dict) -> List[AtencionHistorial]:
        q = self._session.query(EnEsperaDB)
        if filtros.get('fecha_desde'):
            q = q.filter(EnEsperaDB.FechaResolucion >= filtros['fecha_desde'])
        if filtros.get('fecha_hasta'):
            q = q.filter(EnEsperaDB.FechaResolucion <= filtros['fecha_hasta'])
        if filtros.get('seccion'):
            q = q.filter(EnEsperaDB.IdSeccion == filtros['seccion'])
        raws = q.order_by(EnEsperaDB.FechaResolucion.desc()).all()
        return [AtencionHistorial(r.id, r.FechaResolucion, r.IdSeccion, r.Tipo, r.Comentario, r.EstadoFinal, r.TurnoAsignado) for r in raws]

    def cerrar(self):
        self._session.close()