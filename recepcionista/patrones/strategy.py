# 4. recepcionista/patrones/strategy.py
from abc import ABC, abstractmethod

class IOrdenStrategy(ABC):
    @abstractmethod
    def ordenar(self, items: list) -> list: pass

class OrdenAscendente(IOrdenStrategy):
    def ordenar(self, items: list) -> list:
        return sorted(items, key=lambda x: x.fecha)

class OrdenDescendente(IOrdenStrategy):
    def ordenar(self, items: list) -> list:
        return sorted(items, key=lambda x: x.fecha, reverse=True)

