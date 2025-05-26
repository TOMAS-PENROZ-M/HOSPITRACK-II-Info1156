# recepcionista/database_singleton.py

import os
from threading import Lock
from typing import Optional, Protocol
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session, Session


class IDatabase(Protocol):
    """
    Interfaz para abstracción de la conexión a la base de datos.
    Define los métodos que consume la capa de negocio.
    """
    def get_session(self) -> Session:
        ...

    def dispose(self) -> None:
        ...


class DatabaseSingleton(IDatabase):
    """
    Singleton que provee acceso a un motor SQLAlchemy y sesiones.
    Aplica el patrón Singleton (creacional) y Dependency Inversion (DIP).
    """
    _instance: Optional["DatabaseSingleton"] = None
    _lock: Lock = Lock()

    def __new__(cls, db_url: str = None):
        with cls._lock:
            if cls._instance is None:
                if db_url is None:
                    # Por defecto usa SQLite local
                    base = os.path.dirname(__file__)
                    default_path = os.path.join(base, "hospitrack.db")
                    db_url = f"sqlite:///{default_path}"
                cls._instance = super(DatabaseSingleton, cls).__new__(cls)
                cls._instance._initialize(db_url)
            return cls._instance

    def _initialize(self, db_url: str):
        """
        Inicializa el engine y el session factory.
        """
        self._engine = create_engine(
            db_url,
            echo=False,
            connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {}
        )
        # Listener de auditoría (ejemplo Observer)
        @event.listens_for(self._engine, "connect")
        def _on_connect(dbapi_connection, connection_record):
            print(f"[AUDITORÍA] Nueva conexión establecida: {connection_record}")

        # Session factory con scoped_session para hilos
        self._session_factory = scoped_session(
            sessionmaker(
                bind=self._engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False
            )
        )

    def get_session(self) -> Session:
        """
        Retorna una sesión activa; la misma instancia por hilo.
        """
        return self._session_factory()

    def dispose(self) -> None:
        """
        Cierra todas las conexiones y limpia el singleton.
        """
        self._session_factory.remove()
        self._engine.dispose()
        DatabaseSingleton._instance = None

    @classmethod
    def instance(cls, db_url: str = None) -> "DatabaseSingleton":
        """
        Método de fábrica (Factory Method) para obtener el singleton.
        """
        return cls(db_url)
