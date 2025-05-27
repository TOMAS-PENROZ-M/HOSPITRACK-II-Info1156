import sys
import os

# Usar la ruta raiz del proyecto para importar las clases
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import UsuarioDB
from database import get_db

class ControladorRegistro:
    def __init__(self, db_session=next(get_db())):
        self.db_session = db_session

    def registrar_usuario(self, rut, nombre, apellido, correo, telefono, contrasena):
        try:
            # Verificar si el usuario ya existe
            if self.db_session.query(UsuarioDB).filter_by(RUT=rut).first():
                return "El usuario ya existe."

            # Crear un nuevo usuario
            nuevo_usuario = UsuarioDB(
                RUT=rut,
                Nombre=nombre,
                Apellido=apellido,
                CorreoElectronico=correo,
                NumeroTelefono=telefono,
                Contrasenia=contrasena,
                TipoUsuario="UsuarioNormal"  # Por defecto, se asigna el tipo de usuario normal
            )
            self.db_session.add(nuevo_usuario)
            self.db_session.commit()
            return True  # Registro exitoso
        except Exception as e:
            self.db_session.rollback()
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            self.db_session.close()

    def registro_exitoso(self, rut, contrasena):  # Inicia sesión con el usuario recién registrado
        from clases.ControladorLogin import ControladorLogin
        self.controlador_login = ControladorLogin(self.db_session)
        # Inicia sesión con el usuario recién registrado
        return self.controlador_login.iniciar_sesion(rut, contrasena)