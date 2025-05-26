import customtkinter as ctk
from PIL import Image
import tkintermapview
from clases.Mapa import Mapa
from vistas.VistaMapa import VistaMapa
from tkinter import messagebox
from login_registro import LoginRegistroFrame  









ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hospitrack")
        self.geometry("1200x600")

        self.img_folder = "imagenes"
        self.logo_imagen = ctk.CTkImage(Image.open(f"{self.img_folder}/logo.png"), size=(240, 80))

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Marco de navegación
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.grid(row=0, column=0, sticky="nswe")

        self.profile_frame = ctk.CTkFrame(self.nav_frame)
        self.profile_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.profile_frame.grid_rowconfigure(0, weight=1)

        self.iniciar_label = ctk.CTkLabel(self.profile_frame, text="Tiene una cuenta?")
        self.iniciar_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.iniciar_button = ctk.CTkButton(self.profile_frame, text="Iniciar sesión", border_spacing=10, text_color="white", hover_color="seagreen", command=self.mostrar_login_registro)
        self.iniciar_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.registro_label = ctk.CTkLabel(self.profile_frame, text="No tiene una cuenta?")
        self.registro_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.registro_button = ctk.CTkButton(self.profile_frame, text="Registrarse", border_spacing=10, text_color="white", hover_color="seagreen", command=self.mostrar_login_registro)
        self.registro_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Boton para ir al mapa
        self.map_button = ctk.CTkButton(self.nav_frame, text="Mapa", corner_radius=0, border_spacing=10, text_color="white", fg_color="darkseagreen", hover_color="darkseagreen4", command=self.click_nav_mapa)
        self.map_button.grid(row=2, column=0, sticky="ew")

        self.logo_label = ctk.CTkLabel(self.nav_frame, text="", image=self.logo_imagen)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)

        # Contenido principal
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # Vista del mapa (por default al iniciar la app)
        self.vista_mapa = VistaMapa(self.content_frame)


    def color_selected_nav_button(self, boton):
        for button in self.nav_frame.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(fg_color="gray74", hover_color="gray44")
        boton.configure(fg_color="darkseagreen", hover_color="darkseagreen4")
    
    def click_nav_mapa(self):
        self.color_selected_nav_button(self.map_button)
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.vista_mapa = VistaMapa(self.content_frame)

    def mostrar_login_registro(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        login_frame = LoginRegistroFrame(self.content_frame, switch_to_main_callback=self.entrar_a_hospitrack)
        login_frame.grid(row=0, column=0, sticky="nsew")

    def entrar_a_hospitrack(self, usuario):
        messagebox.showinfo("Ingreso", f"Bienvenido a Hospitrack, {usuario.Nombre}")
        # Aquí puedes limpiar el frame y volver al contenido principal si quieres


app = App()
app.mainloop()
