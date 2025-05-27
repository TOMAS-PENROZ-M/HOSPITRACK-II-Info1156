import customtkinter as ctk
from vistas.VistaAdmin import VistaAdmin  
import sys
import os

# Para asegurar de que pueda importar bien los módulos
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Configuración de apariencia
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class AdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Vista Admin Test")
        self.geometry("800x600")

        vista = VistaAdmin(self)
        vista.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()
