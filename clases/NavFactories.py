import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from abc import ABC, abstractmethod
from vistas.VistaMapa import VistaMapa

class NavFactory(ABC):
    @abstractmethod
    def botones_navbar(self):
        pass

    def click_nav_mapa(self, content_frame):
        for widget in content_frame.winfo_children():
            widget.destroy()
        self.vista_mapa = VistaMapa(content_frame)

class NavInvitado(NavFactory):
    def __init__(self):
        self.logged_in = False  # Se mirará este dato para determinar si se crean los botones de inicio de sesión o registro

    def botones_navbar(self):
        return [{"text": "Mapa", "command": self.click_nav_mapa}]
    
    


class NavNormal(NavFactory):
    def __init__(self):
        self.logged_in = True  # Cuando es true no se mostrarán los botones de inicio de sesión ni registro

    def botones_navbar(self):
        return [
            {"text": "Perfil", "command": "click_nav_perfil"},
            {"text": "Mapa", "command": self.click_nav_mapa},
            {"text": "Perfil", "command": "click_nav_perfil"},
            {"text": "Mis Solicitudes", "command": "click_nav_solicitudes"}
        ]

class NavRecepcionista(NavFactory):
    def __init__(self):
        self.logged_in = True  # Cuando es true no se mostrarán los botones de inicio de sesión ni registro

    def botones_navbar(self):
        return [
            {"text": "Perfil", "command": "click_nav_perfil"},
            {"text": "Mapa", "command": self.click_nav_mapa},
            {"text": "Mis Solicitudes", "command": "click_nav_solicitudes"},
            {"text": "Gestionar Solicitudes", "command": "click_nav_gestionar_solicitudes"}
        ]

class NavAdministrador(NavFactory):
    def __init__(self):
        self.logged_in = True  # Cuando es true no se mostrarán los botones de inicio de sesión ni registro

    def botones_navbar(self):
        return [
            {"text": "Perfil", "command": "click_nav_perfil"},
            {"text": "Mapa", "command": self.click_nav_mapa},
            {"text": "Mis Solicitudes", "command": "click_nav_solicitudes"},
            {"text": "Admin", "command": "click_nav_admin"}
        ]