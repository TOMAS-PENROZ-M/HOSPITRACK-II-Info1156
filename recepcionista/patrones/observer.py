from abc import ABC, abstractmethod
# 5. recepcionista/patrones/observer.py
class Observer(ABC):
    @abstractmethod
    def update(self, event:str): pass

class Subject:
    def __init__(self):
        self._observers = []
    def attach(self, obs:Observer): self._observers.append(obs)
    def notify(self, event:str):
        for o in self._observers: o.update(event)

