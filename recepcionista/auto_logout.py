import threading
import logging
import time
from datetime import datetime, timedelta
from typing import Callable, Optional

logger = logging.getLogger("recepcionista.auto_logout")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class AutoLogout:
    """
    Cierra la sesión de usuario después de un periodo de inactividad.
    - timeout_sec: segundos de inactividad antes de logout
    - on_logout: callback llamado tras el logout automático
    """
    def __init__(self, timeout_sec: int = 300, on_logout: Optional[Callable] = None):
        self.timeout_sec = timeout_sec
        self.on_logout = on_logout
        self._timer: Optional[threading.Timer] = None
        self._last_activity: datetime = datetime.utcnow()
        self._lock = threading.Lock()
        self._active = True
        self._start_monitor()

    def _start_monitor(self):
        """
        Inicia el hilo de monitoreo de inactividad.
        """
        logger.debug("Iniciando monitor de AutoLogout (timeout %s sec)", self.timeout_sec)
        self._schedule_timer()

    def _cancel_timer(self):
        """
        Cancela el timer existente si está activo.
        """
        if self._timer and self._timer.is_alive():
            self._timer.cancel()
            logger.debug("Timer de AutoLogout cancelado")

    def _schedule_timer(self):
        """
        Programa un nuevo timer basado en la última actividad registrada.
        """
        with self._lock:
            if not self._active:
                return
            now = datetime.utcnow()
            elapsed = (now - self._last_activity).total_seconds()
            remaining = max(self.timeout_sec - elapsed, 0)
            logger.debug("Programando logout en %s sec", remaining)
            self._cancel_timer()
            self._timer = threading.Timer(remaining, self._trigger_logout)
            self._timer.daemon = True
            self._timer.start()

    def reset_timer(self):
        """
        Debe llamarse tras cada acción de usuario para reiniciar el conteo de inactividad.
        """
        with self._lock:
            self._last_activity = datetime.utcnow()
            logger.debug("AutoLogout: actividad registrada, reiniciando timer")
            self._schedule_timer()

    def _trigger_logout(self):
        """
        Callback interno cuando el timer expira sin actividad.
        """
        with self._lock:
            if not self._active:
                return
            logger.info("AutoLogout: periodo de inactividad excedido (%s sec)", self.timeout_sec)
            self._active = False
        if callable(self.on_logout):
            try:
                self.on_logout()
            except Exception as e:
                logger.exception("Error en callback on_logout: %s", e)
        else:
            logger.warning("No se proporcionó callback on_logout para AutoLogout")

    def stop(self):
        """
        Detiene el monitoreo y cancela timers.
        """
        with self._lock:
            self._active = False
            logger.debug("AutoLogout detenido por petición del usuario")
            self._cancel_timer()

    def is_active(self) -> bool:
        """
        Indica si el AutoLogout sigue en funcionamiento.
        """
        with self._lock:
            return self._active

# Pruebas manuales (solo si se ejecuta directamente)
if __name__ == "__main__":
    expired = []
    def on_logout_cb():
        expired.append(True)
        print("Sesión cerrada automáticamente")

    auto_logout = AutoLogout(timeout_sec=2, on_logout=on_logout_cb)
    print("Simulando actividad... reiniciando timer en 1 seg")
    time.sleep(1)
    auto_logout.reset_timer()
    time.sleep(3)
    print("Expired?", bool(expired))
