import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from abc import ABC, abstractmethod
from vistas.VistaMapa import VistaMapa
from vistas.VistaInicioSesion import VistaInicioSesion
from vistas.VistaRegistro import VistaRegistro

from database import get_db

class NavFactory(ABC):
    @abstractmethod
    def botones_navbar(self):
        pass

    def click_nav_mapa(self, content_frame):
        for widget in content_frame.winfo_children():
            widget.forget()
        if not hasattr(self, 'vista_mapa'):
            self.vista_mapa = VistaMapa(content_frame)
        self.vista_mapa.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

class NavInvitado(NavFactory):
    def __init__(self):
        self.logged_in = False  # Se mirará este dato para determinar si se crean los botones de inicio de sesión o registro

    def botones_navbar(self):
        return [{"text": "Mapa", "command": self.click_nav_mapa}]
    
    def click_nav_iniciar_sesion(self, content_frame):
        for widget in content_frame.winfo_children():
            widget.grid_forget()
        if not hasattr(self, 'vista_inicio_sesion'):
            from clases.ControladorLogin import ControladorLogin
            self.vista_inicio_sesion = VistaInicioSesion(content_frame, ControladorLogin(next(get_db())))
        self.vista_inicio_sesion.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def click_nav_registro(self, content_frame):
        for widget in content_frame.winfo_children():
            widget.grid_forget()
        if not hasattr(self, 'vista_registro'):
            from clases.ControladorRegistro import ControladorRegistro
            self.vista_registro = VistaRegistro(content_frame, ControladorRegistro(next(get_db())))
        self.vista_registro.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")



class NavNormal(NavFactory):
    def __init__(self):
        self.logged_in = True  # Cuando es true no se mostrarán los botones de inicio de sesión ni registro

    def botones_navbar(self):
        return [
            {"text": "Perfil", "command": self.click_nav_perfil},
            {"text": "Mapa", "command": self.click_nav_mapa},
            {"text": "Mis Solicitudes", "command": self.click_nav_solicitudes}
        ]

    def click_nav_perfil(self, content_frame):
        pass

    def click_nav_solicitudes(self, content_frame):
        pass
        

class NavRecepcionista(NavNormal):
    def __init__(self):
        self.logged_in = True  # Cuando es true no se mostrarán los botones de inicio de sesión ni registro

    def botones_navbar(self):
        return [
            {"text": "Perfil", "command": self.click_nav_perfil},
            {"text": "Mapa", "command": self.click_nav_mapa},
            {"text": "Mis Solicitudes", "command": self.click_nav_solicitudes},
            {"text": "Gestionar Solicitudes", "command": self.click_nav_gestionar_solicitudes}
        ]
    
    def click_nav_gestionar_solicitudes(self, content_frame):
        # Este debe llevar a la vista del recepcionista para gestionar solicitudes
        pass

class NavAdministrador(NavNormal):
    def __init__(self):
        self.logged_in = True  # Cuando es true no se mostrarán los botones de inicio de sesión ni registro

    def botones_navbar(self):
        return [
            {"text": "Perfil", "command": self.click_nav_perfil},
            {"text": "Mapa", "command": self.click_nav_mapa},
            {"text": "Mis Solicitudes", "command": self.click_nav_solicitudes},
            {"text": "Admin", "command": self.click_nav_admin}
        ]
    
    def click_nav_admin(self, content_frame):
        for widget in content_frame.winfo_children():
            widget.grid_forget()
        if not hasattr(self, 'vista_admin'):
            from vistas.VistaAdmin import VistaAdmin
            self.vista_admin = VistaAdmin(content_frame)
        self.vista_admin.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")