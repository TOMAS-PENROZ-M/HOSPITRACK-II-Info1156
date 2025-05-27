# recepcionista/db_bridge.py

"""
Puente de base de datos para la vista de recepcionista,
utilizando exactamente la misma configuración que app.py.
Trabaja sobre la tabla EnEsperaDB (fila de espera).
"""

from typing import List
from database import SessionLocal, init_db
from models import EnEsperaDB

class DBBridge:
    """
    Proporciona métodos para:
      - listar todas las entradas de fila de espera
      - aceptar (procesar) una entrada
      - rechazar (descartar) una entrada
      - cerrar la sesión
    """
    def __init__(self):
        # Asegura que existan las tablas
        init_db()
        self._session = SessionLocal()

    def listar_espera(self) -> List[EnEsperaDB]:
        """
        Retorna todas las filas de espera actualmente en la base de datos.
        """
        return (
            self._session
                .query(EnEsperaDB)
                .order_by(EnEsperaDB.HoraRegistro)
                .all()
        )

    def aceptar_entrada(self, entrada_id: int) -> bool:
        """
        Marca una entrada de espera como atendida y la elimina de la fila.
        Retorna True si existía y se procesó; False en caso contrario.
        """
        entrada = self._session.query(EnEsperaDB).get(entrada_id)
        if not entrada:
            return False
        self._session.delete(entrada)
        self._session.commit()
        return True

    def rechazar_entrada(self, entrada_id: int) -> bool:
        """
        Descarta una entrada de espera (rechazada) eliminándola.
        Retorna True si existía y se borró; False en caso contrario.
        """
        entrada = self._session.query(EnEsperaDB).get(entrada_id)
        if not entrada:
            return False
        self._session.delete(entrada)
        self._session.commit()
        return True

    def cerrar(self) -> None:
        """
        Cierra la sesión de la base de datos.
        """
        self._session.close()
