from abc import ABC, abstractmethod
from datetime import datetime

class OrdenEstrategia(ABC):
    @abstractmethod
    def ordenar(self, registros):
        pass

class OrdenAscendente(OrdenEstrategia):
    def ordenar(self, registros):
        return sorted(registros, key=lambda x: x.FechaResolucion or datetime.min)

class OrdenDescendente(OrdenEstrategia):
    def ordenar(self, registros):
        return sorted(registros, key=lambda x: x.FechaResolucion or datetime.min, reverse=True)