import sys
import os
# Asegurarse de que el directorio padre esté en el sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clases.Usuario import SesionApp

class ValidadorSolicitud:
    def __init__(self, seccion, mensaje):
        self.sesion = SesionApp()
        self.seccion = seccion
        self.mensaje = mensaje
    
    def validar(self):
        if not self.sesion.estado.puede_enviar_solicitud():
            raise ValueError("El usuario no tiene permiso para enviar solicitudes.")
        if not self.seccion:
            raise ValueError("Debe seleccionar una sección para enviar la solicitud.")
        if not self.mensaje:
            raise ValueError("El mensaje de la solicitud no puede estar vacío.")