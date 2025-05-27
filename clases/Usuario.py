import sys
import os

# Usar la ruta raiz del proyecto para importar las clases
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from abc import ABC, abstractmethod
from database import get_db
from models import UsuarioDB, SeccionDB, SolicitudDB
from clases.States import EstadoInvitado
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
    
    def solicitar_atencion(self, mensaje, seccion):  # La sección será selected_seccion del mapa
        db = next(get_db())
        # Esto se activara solo despues de haber validado la solicitud
        seccion_db = db.query(SeccionDB).filter(SeccionDB.IdSeccion == seccion.id).first()
        if seccion_db:
            from datetime import datetime
            try:
                soli = SolicitudDB(
                    RUT=self.rut,
                    IdSeccion=seccion_db.IdSeccion,
                    Mensaje=mensaje,
                    HoraSolicitud=datetime.now(),
                    Estado="Pendiente"
                )
                db.add(soli)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                print(f"Error al enviar solicitud: {e}")
                return False

class Recepcionista(Usuario):
    def __init__(self, rut):
        super().__init__(rut, "recepcionista")
        
    
    def obtener_seccion(self):
        pass

class Administrador(Usuario):
    def __init__(self, rut):
        super().__init__(rut, "administrador")


class SesionApp:
    # Singleton para manejar la sesión de la aplicación, solo debe haber una instancia de SesionApp en toda la aplicación
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(SesionApp, cls).__new__(cls)
            cls.usuario_actual = None  # Almacena el usuario actual
            cls.estado = EstadoInvitado()   # Patron State (por implementar)
        return cls._instancia

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