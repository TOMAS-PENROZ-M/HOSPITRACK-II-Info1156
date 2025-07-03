import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.NavFactories import *
from typing import Protocol

class Estado(Protocol):
    def puede_enviar_solicitud(self):
        """Determina si el usuario puede enviar una solicitud."""
        pass

    def nav_factory(self):
        """Devuelve la fábrica de navegación correspondiente al estado del usuario."""
        pass

# Estado base
class EstadoInvitado(Estado):
    def puede_enviar_solicitud(self):
        return False
    
    def nav_factory(self):
        return NavInvitado()

# Usuario normal
class EstadoNormal(Estado):
    def puede_enviar_solicitud(self):
        return True

    def nav_factory(self):
        return NavNormal()

# Usuario suspendido
class EstadoSuspendido(Estado):
    def puede_enviar_solicitud(self):
        return False
    
    def nav_factory(self):
        return NavNormal()

# Recepcionista
class EstadoRecepcionista(EstadoNormal):    # Puede enviar solicitudes como usuario normal
    def nav_factory(self):
        return NavRecepcionista()

# Administrador
class EstadoAdministrador(EstadoNormal):  # Puede enviar solicitudes como usuario normal
    def nav_factory(self):
        return NavAdministrador()