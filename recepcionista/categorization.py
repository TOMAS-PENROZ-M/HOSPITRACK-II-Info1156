import logging
from enum import Enum
from typing import Any, List, Dict, Union

# Configuración de logging para categorización
logger = logging.getLogger("recepcionista.categorization")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class Priority(Enum):
    BAJA = 'Baja'
    MEDIA = 'Media'
    ALTA = 'Alta'
    CRITICA = 'Crítica'
    URGENTE = 'Urgente'

class CategorizationError(Exception):
    """
    Excepción lanzada cuando ocurre un error de categorización.
    """
    pass

class Categorizer:
    """
    Sistema de categorización de solicitudes por prioridad.

    Métodos:
        - categorize: devuelve una Priority para una solicitud.
        - batch_categorize: categoriza una lista de solicitudes.
        - priority_to_int: obtiene un valor numérico para comparaciones.
    """
    # Umbrales de longitud de descripción para prioridades
    _length_thresholds: Dict[Priority, int] = {
        Priority.URGENTE: 500,
        Priority.CRITICA: 250,
        Priority.ALTA: 100,
        Priority.MEDIA: 50,
        Priority.BAJA: 0,
    }

    def __init__(self):
        self.thresholds = self._length_thresholds
        logger.debug("Categorizer inicializado con thresholds %s", self.thresholds)

    def categorize(self, solicitud: Any) -> Priority:
        """
        Asigna prioridad basada en atributos de 'solicitud'.

        Criterios:
        1. Si tiene marca 'es_urgente' True -> URGENTE
        2. Si la descripción supera thresholds -> CRÍTICA, ALTA, MEDIA, BAJA
        3. Si solicitud tiene campo 'impacto' alto -> CRÍTICA
        4. Otros parámetros personalizados.
        """
        try:
            if hasattr(solicitud, 'es_urgente') and solicitud.es_urgente:
                logger.debug("Solicitud %s marcada como URGENTE", solicitud.id)
                return Priority.URGENTE

            desc = getattr(solicitud, 'descripcion', '')
            length = len(desc or '')

            for priority, threshold in sorted(self.thresholds.items(), key=lambda x: -x[1]):
                if length >= threshold:
                    logger.debug(
                        "Solicitud %s categorizada como %s (length=%d threshold=%d)",
                        getattr(solicitud, 'id', None), priority.name, length, threshold
                    )
                    return priority

            # Criterio adicional basado en impacto si existe
            impacto = getattr(solicitud, 'impacto', None)
            if impacto:
                if impacto.lower() in ('alto', 'crítico'):
                    logger.debug("Solicitud %s impacto alto detectado", solicitud.id)
                    return Priority.CRITICA

            # Por defecto, BAJA
            logger.debug("Solicitud %s por defecto prioridad BAJA", solicitud.id)
            return Priority.BAJA

        except Exception as e:
            logger.exception("Error categorizando solicitud: %s", e)
            raise CategorizationError(f"Error categorizando solicitud: {e}")

    def batch_categorize(self, solicitudes: List[Any]) -> Dict[Any, Priority]:
        """
        Categorización en lote: devuelve mapping id_solicitud -> Priority.
        """
        result: Dict[Any, Priority] = {}
        for sol in solicitudes:
            try:
                pri = self.categorize(sol)
                result[getattr(sol, 'id', sol)] = pri
            except CategorizationError as ce:
                logger.error("No se pudo categorizar solicitud %s: %s", getattr(sol, 'id', None), ce)
        return result

    @staticmethod
    def priority_to_int(priority: Priority) -> int:
        """
        Convierte Priority a valor entero para comparaciones.
        Urgente=5, Crítica=4, Alta=3, Media=2, Baja=1.
        """
        mapping = {
            Priority.URGENTE: 5,
            Priority.CRITICA: 4,
            Priority.ALTA: 3,
            Priority.MEDIA: 2,
            Priority.BAJA: 1,
        }
        val = mapping.get(priority)
        if val is None:
            logger.warning("Priority %s no mapeada, asumiendo valor 1", priority)
            return 1
        return val

# Pruebas manuales si se ejecuta directamente
if __name__ == '__main__':
    class Dummy:
        def __init__(self, id, desc, es_urgente=False, impacto=None):
            self.id = id
            self.descripcion = desc
            self.es_urgente = es_urgente
            self.impacto = impacto

    cat = Categorizer()
    muestras = [
        Dummy(1, 'x'*10),
        Dummy(2, 'y'*60),
        Dummy(3, 'z'*120),
        Dummy(4, 'w'*300),
        Dummy(5, 'u'*600),
        Dummy(6, 'desc corta', es_urgente=True),
        Dummy(7, 'desc mediana', impacto='alto'),
    ]
    resultado = cat.batch_categorize(muestras)
    for k, v in resultado.items():
        print(f"Solicitud {k} -> Prioridad {v.value} ({Categorizer.priority_to_int(v)})")
