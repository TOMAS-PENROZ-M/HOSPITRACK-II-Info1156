import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import UsuarioDB
from database import get_db
from seguridad import hashear_contrasena  

class ControladorRegistro:
    def __init__(self, db_session=next(get_db())):
        self.db_session = db_session

    def registrar_usuario(self, rut, nombre, apellido, correo, telefono, contrasena):
        try:
            if self.db_session.query(UsuarioDB).filter_by(RUT=rut).first():
                return "El usuario ya existe."

            # Hashear 
            contrasena_segura = hashear_contrasena(contrasena)

            nuevo_usuario = UsuarioDB(
                RUT=rut,
                Nombre=nombre,
                Apellido=apellido,
                CorreoElectronico=correo,
                NumeroTelefono=telefono,
                Contrasenia=contrasena_segura,
                TipoUsuario="UsuarioNormal"
            )
            self.db_session.add(nuevo_usuario)
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            self.db_session.close()

    def registro_exitoso(self, rut, contrasena):
        from clases.ControladorLogin import ControladorLogin
        self.controlador_login = ControladorLogin(self.db_session)
        return self.controlador_login.iniciar_sesion(rut, contrasena)
