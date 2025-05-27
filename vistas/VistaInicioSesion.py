import sys
import os
# Asegurarse de que el directorio padre esté en el sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from clases.ControladorLogin import ControladorLogin

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
            # Aquí se llamaría al controlador para iniciar sesión
            resultado = self.controlador_login.iniciar_sesion(rut, contrasena)
            if resultado:
                usuario, estado = resultado
                self.sesion_iniciada(usuario, estado)  # Cambia el estado de la sesión, como es singleton, se puede acceder directamente
        else:
            ctk.CTkMessageBox.show_error("Error", "Por favor, complete todos los campos.")

    def sesion_iniciada(self, usuario, estado):   # Agrega el usuario y el estado a la sesión
        self.controlador_login.sesion_iniciada(usuario, estado)