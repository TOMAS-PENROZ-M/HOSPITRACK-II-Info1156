from abc import ABC, abstractmethod
from datetime import datetime

class IOrdenStrategy(ABC):
    @abstractmethod
    def ordenar(self, items: list) -> list: pass

class OrdenAscendente(IOrdenStrategy):
    def ordenar(self, items: list) -> list:
        default_date = datetime.max  # Fecha muy futura para None
        return sorted(items, key=lambda x: x.fecha if x.fecha is not None else default_date)

class OrdenDescendente(IOrdenStrategy):
    def ordenar(self, items: list) -> list:
        default_date = datetime.min  # Fecha muy antigua para None
        return sorted(items, key=lambda x: x.fecha if x.fecha is not None else default_date, reverse=True)