# 6. recepcionista/patrones/rule_engine.py
from datetime import datetime, time

class RuleEngine:
    def __init__(self):
        self.turnos = [
            ('Mañana', time(8,0), time(12,0)),
            ('Tarde', time(12,0), time(17,0)),
            ('Noche', time(17,0), time(22,0)),
        ]
    def assign(self, solicitud) -> str:
        hora = solicitud.hora_solicitud
        prioridad = solicitud.prioridad.lower()
        # Alta prioridad => turno actual
        if prioridad=='alta':
            for n,i,f in self.turnos:
                if i<=hora.time()<f: return n
            return self.turnos[0][0]
        # Media prioridad => siguiente
        if prioridad=='media':
            for idx,(n,i,f) in enumerate(self.turnos):
                if i<=hora.time()<f:
                    return self.turnos[(idx+1)%len(self.turnos)][0]
            return self.turnos[1][0]
        # Baja prioridad => noche
        if prioridad=='baja': return 'Noche'
        # Default por hora
        for n,i,f in self.turnos:
            if i<=hora.time()<f: return n
        return self.turnos[0][0]
