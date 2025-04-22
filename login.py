
import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
#orden usuario,clave,host
engine = create_engine("mysql+mysqlconnector://hospitrack:hospitrack@localhost/hospitrack")
Session = sessionmaker(bind=engine)


class Usuario(Base):
    __tablename__ = 'dsoftware_usuario'

    RUT = Column(String(9), primary_key=True)
    Nombre = Column(String(50))
    Apellido = Column(String(50))
    CorreoElectronico = Column(String(75))
    NumeroTelefono = Column(String(9))
    TipoUsuario = Column(String(20))
    Contrasenia = Column(String(255))
    fotourl = Column(String(255))


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Inicio de Sesión")
        self.geometry("400x400")

        self.label_titulo = ctk.CTkLabel(self, text="Iniciar Sesión", font=("Arial", 20))
        self.label_titulo.pack(pady=20)

        self.rut_entry = ctk.CTkEntry(self, placeholder_text="RUT")
        self.rut_entry.pack(pady=10)

        self.contrasena_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.contrasena_entry.pack(pady=10)

        self.boton_login = ctk.CTkButton(self, text="Ingresar", command=self.iniciar_sesion)
        self.boton_login.pack(pady=20)

    def iniciar_sesion(self):
        rut = self.rut_entry.get()
        contrasena = self.contrasena_entry.get()

        session = Session()
        try:
            usuario = session.query(Usuario).filter_by(RUT=rut, Contrasenia=contrasena).first()
            if usuario:
                messagebox.showinfo("Bienvenido", f"Hola {usuario.Nombre}, ingresaste como {usuario.TipoUsuario}")
              
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo validar: {e}")
        finally:
            session.close()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
