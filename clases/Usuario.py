import sys
import os

# Usar la ruta raiz del proyecto para importar las clases
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from abc import ABC, abstractmethod
from database import get_db
from models import UsuarioDB, SeccionDB
from clases.States import EstadoInvitado

# PATRÓN OBSERVER
# -------------------------------
class Observer(ABC):
    @abstractmethod
    def actualizar(self, estado):
        pass

class Observable:
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        self._observadores.append(observador)

    def eliminar_observador(self, observador):
        self._observadores.remove(observador)

    def notificar_observadores(self):
        for observador in self._observadores:
            observador.actualizar(self.estado)




class Usuario(ABC):
    def __init__(self, rut, tipousuario):
        # El rut nunca debería cambiar, por lo que se guarda para obtener informacion de la base de datos
        self.__rut = rut
        self.__tipousuario = tipousuario
    
    @property
    def rut(self):
        return self.__rut

    @property
    def tipousuario(self):
        return self.__tipousuario
    
    def obtener_info(self):
        # Consulta la información del usuario en la base de datos
        db = next(get_db())
        usuario = db.query(UsuarioDB).filter(UsuarioDB.RUT == self.__rut).first()
        return usuario

class UsuarioNormal(Usuario):
    def __init__(self, rut):
        super().__init__(rut, "normal")
    
    def solicitar_atencion(self, mensaje):  # La sección será selected_seccion del mapa
        # Implementar lógica para solicitar atención
        pass

class Recepcionista(Usuario):
    def __init__(self, rut):
        super().__init__(rut, "recepcionista")
        
    
    def obtener_seccion(self):
        pass

class Administrador(Usuario):
    def __init__(self, rut):
        super().__init__(rut, "administrador")


# SESIÓN SINGLETON + OBSERVABLE
# -------------------------------
class SesionApp(Observable):
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(SesionApp, cls).__new__(cls)
            cls._instancia.__initialized = False
        return cls._instancia

    def __init__(self):
        if not self.__initialized:
            super().__init__()  # Inicializa Observable
            self.usuario_actual = None
            self.estado = EstadoInvitado()
            self.__initialized = True

    def cambiar_estado(self, usuario, estado):
        self.usuario_actual = usuario
        self.estado = estado
        self.notificar_observadores()

if __name__ == "__main__":
    sesion = SesionApp()
    usuario = "pedrito"
    sesion.usuario_actual = usuario
    print(sesion.usuario_actual)  # Debería imprimir "pedrito"

    print(sesion is SesionApp())  # Debería imprimir True, confirmando que es un singleton

    sesion2 = SesionApp()
    print(sesion2 is sesion)  # Debería imprimir True, confirmando que sesion2 es la misma instancia que sesion
    sesion2.usuario_actual = "juanito"
    print(sesion.usuario_actual)  # Debería imprimir "juanito", ya que sesion2 es la misma instancia que sesion