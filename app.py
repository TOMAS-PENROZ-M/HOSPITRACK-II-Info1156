import customtkinter as ctk
from PIL import Image
import tkintermapview
from vistas.VistaMapa import VistaMapa
from clases.Usuario import SesionApp, Observer  # Importamos Observer
from tkinter import messagebox

class App(ctk.CTk, Observer):
    def __init__(self):
        super().__init__()
        self.title("Hospitrack")
        self.geometry("1200x600")

        # Sesión de la aplicación
        self.sesion = SesionApp()
        self.sesion.agregar_observador(self)  # Se registra como observer

        self.img_folder = "imagenes"
        self.logo_imagen = ctk.CTkImage(Image.open(f"{self.img_folder}/logo.png"), size=(240, 80))

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.grid(row=0, column=0, sticky="nswe")

        self.logo_label = ctk.CTkLabel(self.nav_frame, text="", image=self.logo_imagen)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        self.vista_mapa = VistaMapa(self.content_frame)
        self.vista_mapa.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.crear_menu_navegacion()

    def crear_menu_navegacion(self):
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        self.logo_label = ctk.CTkLabel(self.nav_frame, text="", image=self.logo_imagen)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)

        factory = self.sesion.estado.nav_factory()
        if not factory.logged_in:
            self.login_frame = ctk.CTkFrame(self.nav_frame)
            self.login_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

            self.iniciar_label = ctk.CTkLabel(self.login_frame, text="Tiene una cuenta?")
            self.iniciar_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            self.iniciar_button = ctk.CTkButton(
                self.login_frame, text="Iniciar sesión",
                border_spacing=10, text_color="white", hover_color="seagreen",
                command=lambda: factory.click_nav_iniciar_sesion(self.content_frame)
            )
            self.iniciar_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            self.registro_label = ctk.CTkLabel(self.login_frame, text="No tiene una cuenta?")
            self.registro_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
            self.registro_button = ctk.CTkButton(
                self.login_frame, text="Registrarse",
                border_spacing=10, text_color="white", hover_color="seagreen",
                command=lambda: factory.click_nav_registro(self.content_frame)
            )
            self.registro_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        for botoncito in factory.botones_navbar():
            boton = ctk.CTkButton(
                self.nav_frame, text=botoncito["text"],
                corner_radius=0, border_spacing=10, text_color="white",
                fg_color="darkseagreen", hover_color="darkseagreen4",
                command=lambda: botoncito["command"](self.content_frame)
            )
            boton.grid(row=2, column=0, sticky="ew")

    def actualizar(self, nuevo_estado):
        # Esto se llama automáticamente cuando el estado cambia
        self.crear_menu_navegacion()

    def color_selected_nav_button(self, boton):
        for button in self.nav_frame.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(fg_color="gray74", hover_color="gray44")
        boton.configure(fg_color="darkseagreen", hover_color="darkseagreen4")

app = App()
app.mainloop()
