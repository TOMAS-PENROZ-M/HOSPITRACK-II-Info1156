from database import get_db
from models import UsuarioDB

class UsuarioService:

    def obtener_usuario(self, rut_usuario):
        session = next(get_db())
        try:
            usuario = session.query(UsuarioDB).filter_by(RUT=rut_usuario).first()
            return usuario
        finally:
            session.close()

    def actualizar_usuario(self, rut_usuario, correo, telefono):
        session = next(get_db())
        try:
            usuario = session.query(UsuarioDB).filter_by(RUT=rut_usuario).first()
            if usuario:
                usuario.CorreoElectronico = correo
                usuario.NumeroTelefono = telefono
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()