# recepcionista/categorization.py

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Protocol


class Prioridad(Enum):
    URGENTE = "Urgente"
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"


class SolicitudCategorizable(Protocol):
    """
    Protocolo que define la interfaz mínima para
    una solicitud que se puede categorizar.
    """
    id: int
    titulo: str
    descripcion: str
    es_urgente: bool


class ReglaCategorizacion(ABC):
    """
    Regla base para categorización de solicitudes.
    Cada regla revisa la solicitud y, si aplica, devuelve una prioridad.
    """
    @abstractmethod
    def aplica(self, solicitud: SolicitudCategorizable) -> bool:
        """
        Indica si la regla es aplicable para esta solicitud.
        """
        pass

    @abstractmethod
    def prioridad(self) -> Prioridad:
        """
        Prioridad que asigna esta regla.
        """
        pass


class ReglaUrgenciaEspecifica(ReglaCategorizacion):
    """
    Si la solicitud viene marcada como urgente explícitamente.
    """
    def aplica(self, solicitud: SolicitudCategorizable) -> bool:
        return getattr(solicitud, "es_urgente", False)

    def prioridad(self) -> Prioridad:
        return Prioridad.URGENTE


class ReglaPalabrasClave(ReglaCategorizacion):
    """
    Reglas basadas en presencia de palabras clave en título o descripción.
    """
    def __init__(self, palabras: List[str], prioridad: Prioridad):
        self.palabras = [p.lower() for p in palabras]
        self._prioridad = prioridad

    def aplica(self, solicitud: SolicitudCategorizable) -> bool:
        texto = f"{solicitud.titulo} {solicitud.descripcion}".lower()
        return any(p in texto for p in self.palabras)

    def prioridad(self) -> Prioridad:
        return self._prioridad


class ReglaLongitudDescripcion(ReglaCategorizacion):
    """
    Usa la longitud de la descripción para determinar prioridad.
    """
    def __init__(self, umbral: int, prioridad: Prioridad):
        self.umbral = umbral
        self._prioridad = prioridad

    def aplica(self, solicitud: SolicitudCategorizable) -> bool:
        return len(solicitud.descripcion or "") >= self.umbral

    def prioridad(self) -> Prioridad:
        return self._prioridad


class Categorizador:
    """
    Compositor de reglas de categorización. Sigue Open/Closed:
    puede recibir nuevas reglas sin modificar la clase.
    """
    def __init__(self):
        self.reglas: List[ReglaCategorizacion] = []
        self._inicializar_reglas()

    def _inicializar_reglas(self):
        # Regla explícita de urgencia
        self.reglas.append(ReglaUrgenciaEspecifica())

        # Palabras clave para prioridad alta
        self.reglas.append(ReglaPalabrasClave(
            palabras=["emergencia", "grave", "accidente", "inmediato"],
            prioridad=Prioridad.URGENTE
        ))
        self.reglas.append(ReglaPalabrasClave(
            palabras=["importante", "prioritario"], prioridad=Prioridad.ALTA
        ))
        # Palabras clave para prioridad media
        self.reglas.append(ReglaPalabrasClave(
            palabras=["dolor", "consulta", "fiebre", "malestar"],
            prioridad=Prioridad.MEDIA
        ))
        # Longitud para prioridad alta
        self.reglas.append(ReglaLongitudDescripcion(
            umbral=300, prioridad=Prioridad.ALTA
        ))
        # Longitud para prioridad media
        self.reglas.append(ReglaLongitudDescripcion(
            umbral=100, prioridad=Prioridad.MEDIA
        ))

    def categorizar(self, solicitud: SolicitudCategorizable) -> Prioridad:
        """
        Recorre las reglas en orden y devuelve la prioridad
        de la primera que aplica. Por defecto, BAJA.
        """
        for regla in self.reglas:
            if regla.aplica(solicitud):
                return regla.prioridad()
        return Prioridad.BAJA


# Ejemplo de uso y prueba sencilla
if __name__ == "__main__":
    class EjemploSolicitud:
        def __init__(self, id, titulo, descripcion, es_urgente=False):
            self.id = id
            self.titulo = titulo
            self.descripcion = descripcion
            self.es_urgente = es_urgente

    ejemplos = [
        EjemploSolicitud(1, "Consulta normal", "Quiero información sobre mi cita.", False),
        EjemploSolicitud(2, "Emergencia", "Sufro un accidente grave ahora.", False),
        EjemploSolicitud(3, "Malestar", "Tengo dolor y fiebre desde ayer.", False),
        EjemploSolicitud(4, "Comentario largo", "x" * 150, False),
        EjemploSolicitud(5, "Muy largo", "y" * 350, False),
        EjemploSolicitud(6, "Revisión", "Todo bien", True),
    ]

    categorizador = Categorizador()
    for s in ejemplos:
        print(f"Solicitud {s.id} -> {categorizador.categorizar(s).value}")
