import sys
import os

# Usar la ruta raiz del proyecto para importar las clases
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tkinter import messagebox
from database import get_db
from models import UsuarioDB

class ControladorLogin:
    def __init__(self, db_session=next(get_db())):
        self.db_session = db_session
    
    def iniciar_sesion(self, rut, contrasena):
        try:
            usuario_db = self.db_session.query(UsuarioDB).filter_by(RUT=rut, Contrasenia=contrasena).first()
            if usuario_db:
                from clases.Usuario import UsuarioNormal, Recepcionista, Administrador
                from clases.States import EstadoNormal, EstadoRecepcionista, EstadoAdministrador, EstadoSuspendido
                if usuario_db.TipoUsuario == "Suspendido":
                    state = EstadoSuspendido()
                    usuario = UsuarioNormal(rut)  # Se crea un usuario normal para obtener la información
                    return usuario, state
                elif usuario_db.TipoUsuario == "Recepcionista":
                    state = EstadoRecepcionista()
                    usuario = Recepcionista(rut)
                    return usuario, state
                elif usuario_db.TipoUsuario == "Administrador":
                    state = EstadoAdministrador()
                    usuario = Administrador(rut)
                    return usuario, state
                else:  # Usuario normal
                    state = EstadoNormal()
                    usuario = UsuarioNormal(rut)
                    return usuario, state
                
            else:
                messagebox.showerror("Error", "Credenciales incorrectas.")
        except Exception as e:
            Exception(f"Error al iniciar sesión: {e}")
            self.db_session.rollback()
            messagebox.showerror("Error", str(e))
            return None
        finally:
            self.db_session.close()

    def sesion_iniciada(self, usuario, state):
        from clases.Usuario import SesionApp
        sesion = SesionApp()
        sesion.usuario_actual = usuario
        sesion.estado = state
        messagebox.showinfo("Bienvenido", f"Hola {usuario.obtener_info().Nombre}, rol: {usuario.tipousuario}")
        return True