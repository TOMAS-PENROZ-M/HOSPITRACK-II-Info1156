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

class RegistroApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Registro de Usuario")
        self.geometry("400x600")

        self.rut = ctk.CTkEntry(self, placeholder_text="RUT")
        self.rut.pack(pady=10)

        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre")
        self.nombre.pack(pady=10)

        self.apellido = ctk.CTkEntry(self, placeholder_text="Apellido")
        self.apellido.pack(pady=10)

        self.correo = ctk.CTkEntry(self, placeholder_text="Correo Electrónico")
        self.correo.pack(pady=10)

        self.telefono = ctk.CTkEntry(self, placeholder_text="Número de Teléfono")
        self.telefono.pack(pady=10)

        self.tipo_usuario = ctk.CTkOptionMenu(self, values=["Admin", "UsuarioNormal", "Recepcionista"])
        self.tipo_usuario.set("UsuarioNormal")
        self.tipo_usuario.pack(pady=10)

        self.contrasena = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.contrasena.pack(pady=10)

        self.fotourl = ctk.CTkEntry(self, placeholder_text="URL de Foto")
        self.fotourl.pack(pady=10)

        self.btn_registrar = ctk.CTkButton(self, text="Registrarse", command=self.registrar_usuario)
        self.btn_registrar.pack(pady=20)

    def registrar_usuario(self):
        nuevo_usuario = Usuario(
            RUT=self.rut.get(),
            Nombre=self.nombre.get(),
            Apellido=self.apellido.get(),
            CorreoElectronico=self.correo.get(),
            NumeroTelefono=self.telefono.get(),
            TipoUsuario=self.tipo_usuario.get(),
            Contrasenia=self.contrasena.get(),
            fotourl=self.fotourl.get()
        )

        session = Session()
        try:
            session.add(nuevo_usuario)
            session.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            session.close()

if __name__ == "__main__":
    app = RegistroApp()
    app.mainloop()
