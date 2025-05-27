import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import UsuarioDB
from database import get_db

# Base de datos
Base = declarative_base()




class LoginRegistroFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to_main_callback):
        super().__init__(master)
        self.switch_to_main_callback = switch_to_main_callback

        self.grid_columnconfigure(0, weight=1)
        self.login_frame = self.crear_login_frame()
        self.registro_frame = self.crear_registro_frame()

        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.registro_frame.grid(row=0, column=0, sticky="nsew")
        self.mostrar_login()

    def crear_login_frame(self):
        frame = ctk.CTkFrame(self)

        ctk.CTkLabel(frame, text="Iniciar Sesión", font=("Arial", 20)).pack(pady=10)
        self.login_rut = ctk.CTkEntry(frame, placeholder_text="RUT")
        self.login_rut.pack(pady=5)

        self.login_contrasena = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*")
        self.login_contrasena.pack(pady=5)

        ctk.CTkButton(frame, text="Ingresar", command=self.iniciar_sesion).pack(pady=10)
        ctk.CTkButton(frame, text="Ir a Registro", command=self.mostrar_registro).pack(pady=5)

        return frame

    def crear_registro_frame(self):
        frame = ctk.CTkFrame(self)

        ctk.CTkLabel(frame, text="Registro de Usuario", font=("Arial", 20)).pack(pady=10)

        self.reg_rut = ctk.CTkEntry(frame, placeholder_text="RUT")
        self.reg_rut.pack(pady=5)

        self.reg_nombre = ctk.CTkEntry(frame, placeholder_text="Nombre")
        self.reg_nombre.pack(pady=5)

        self.reg_apellido = ctk.CTkEntry(frame, placeholder_text="Apellido")
        self.reg_apellido.pack(pady=5)

        self.reg_correo = ctk.CTkEntry(frame, placeholder_text="Correo Electrónico")
        self.reg_correo.pack(pady=5)

        self.reg_telefono = ctk.CTkEntry(frame, placeholder_text="Teléfono")
        self.reg_telefono.pack(pady=5)

        self.reg_tipo = ctk.CTkOptionMenu(frame, values=["Admin", "UsuarioNormal", "Recepcionista"])
        self.reg_tipo.set("UsuarioNormal")
        self.reg_tipo.pack(pady=5)

        self.reg_contra = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*")
        self.reg_contra.pack(pady=5)

        self.reg_foto = ctk.CTkEntry(frame, placeholder_text="URL de Foto")
        self.reg_foto.pack(pady=5)

        ctk.CTkButton(frame, text="Registrarse", command=self.registrar_usuario).pack(pady=10)
        ctk.CTkButton(frame, text="Volver al Login", command=self.mostrar_login).pack(pady=5)

        return frame

    def mostrar_login(self):
        self.registro_frame.grid_forget()
        self.login_frame.grid(row=0, column=0, sticky="nsew")

    def mostrar_registro(self):
        self.login_frame.grid_forget()
        self.registro_frame.grid(row=0, column=0, sticky="nsew")

    def iniciar_sesion(self):
        rut = self.login_rut.get()
        contra = self.login_contrasena.get()

        session = next(get_db())
        try:
            usuario = session.query(UsuarioDB).filter_by(RUT=rut, Contrasenia=contra).first()
            if usuario:
                messagebox.showinfo("Bienvenido", f"Hola {usuario.Nombre}, rol: {usuario.TipoUsuario}")
                self.switch_to_main_callback(usuario)
            else:
                messagebox.showerror("Error", "Credenciales incorrectas.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            session.close()

    def registrar_usuario(self):
        nuevo = UsuarioDB(
            RUT=self.reg_rut.get(),
            Nombre=self.reg_nombre.get(),
            Apellido=self.reg_apellido.get(),
            CorreoElectronico=self.reg_correo.get(),
            NumeroTelefono=self.reg_telefono.get(),
            TipoUsuario=self.reg_tipo.get(),
            Contrasenia=self.reg_contra.get(),
            fotourl=self.reg_foto.get()
        )

        session = next(get_db())
        try:
            session.add(nuevo)
            session.commit()
            messagebox.showinfo("Registro exitoso", "Usuario creado correctamente.")
            self.mostrar_login()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            session.close()
