import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from clases.ControladorLogin import ControladorLogin
from clases.Usuario import SesionApp  # Importamos SesionApp

class VistaInicioSesion(ctk.CTkFrame):
    def __init__(self, master, controlador_login=ControladorLogin):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.controlador_login = controlador_login

        # Frame de inicio de sesión
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.login_frame, text="Iniciar Sesión", font=("Arial", 20)).pack(pady=10)

        self.rut_entry = ctk.CTkEntry(self.login_frame, placeholder_text="RUT")
        self.rut_entry.pack(pady=5)

        self.contrasena_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Contraseña", show="*")
        self.contrasena_entry.pack(pady=5)

        ctk.CTkButton(self.login_frame, text="Ingresar", command=self.iniciar_sesion).pack(pady=10)
    
    def iniciar_sesion(self):
        rut = self.rut_entry.get()
        contrasena = self.contrasena_entry.get()
        if rut and contrasena:
            resultado = self.controlador_login.iniciar_sesion(rut, contrasena)
            if resultado:
                usuario, estado = resultado
                sesion = SesionApp()
                sesion.cambiar_estado(usuario, estado)  # Ahora notifica a observadores
        else:
            ctk.CTkMessageBox.show_error("Error", "Por favor, complete todos los campos.")
