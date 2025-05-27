import sys
import os
# Asegurarse de que el directorio padre esté en el sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from clases.ControladorRegistro import ControladorRegistro

class VistaRegistro(ctk.CTkFrame):
    def __init__(self, master, controlador_registro=ControladorRegistro):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.controlador_registro = controlador_registro

        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

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

        self.reg_contra = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*")
        self.reg_contra.pack(pady=5)


        ctk.CTkButton(frame, text="Registrarse", command=self.registrar_usuario).pack(pady=10)

    def registrar_usuario(self):    # Por default tipo usuario Normal
        rut = self.reg_rut.get()
        nombre = self.reg_nombre.get()
        apellido = self.reg_apellido.get()
        correo = self.reg_correo.get()
        telefono = self.reg_telefono.get()
        contrasena = self.reg_contra.get()

        if rut and nombre and apellido and correo and telefono and contrasena:
            resultado = self.controlador_registro.registrar_usuario(rut, nombre, apellido, correo, telefono, contrasena)
            if resultado is True:
                self.controlador_registro.registro_exitoso(rut, contrasena)  # Inicia sesión automáticamente