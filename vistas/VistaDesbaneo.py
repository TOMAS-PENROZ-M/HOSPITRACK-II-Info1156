from database import get_db
from models import UsuarioDB

class GestorDesbaneo:
    def __init__(self):
        self.db = next(get_db())

    def desbanear_usuario(self, rut):
        try:
            usuario = self.db.query(UsuarioDB).filter_by(RUT=rut).first()
            if usuario and usuario.TipoUsuario == "Suspendido":
                usuario.TipoUsuario = "UsuarioNormal"  # o su tipo anterior si lo guardas
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            print(f"Error al desbanear: {e}")
            return False
        finally:
            self.db.close()
