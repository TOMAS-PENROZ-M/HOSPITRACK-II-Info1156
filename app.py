import customtkinter as ctk
from PIL import Image
import tkintermapview
from clases.Mapa import Mapa
from vistas.VistaMapa import VistaMapa
from tkinter import messagebox
from login_registro import LoginRegistroFrame  
from clases.Usuario import *

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hospitrack")
        self.geometry("1200x600")

        # Sesión de la aplicación
        self.sesion = SesionApp()   # Por defecto invitado, se cambiará al iniciar sesión o registrarse

        # Sesión de la aplicación
        self.sesion = SesionApp()   # Por defecto invitado, se cambiará al iniciar sesión o registrarse

        self.img_folder = "imagenes"
        self.logo_imagen = ctk.CTkImage(Image.open(f"{self.img_folder}/logo.png"), size=(240, 80))

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Marco de navegación
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.grid(row=0, column=0, sticky="nswe")

        self.logo_label = ctk.CTkLabel(self.nav_frame, text="", image=self.logo_imagen)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)

        self.crear_menu_navegacion()


        # Contenido principal, a la derecha --------------------------------------------------------------------------------------
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # Vista del mapa (por default al iniciar la app)
        self.vista_mapa = VistaMapa(self.content_frame)
    
    def crear_menu_navegacion(self):
        # Crear los elementos de navegación según el estado del usuario
        # esto de acá es desde el logo para abajo
        factory = self.sesion.estado.nav_factory()
        if not factory.logged_in:
            self.login_frame = ctk.CTkFrame(self.nav_frame)
            self.login_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
            self.login_frame.grid_rowconfigure(0, weight=1)
            # Al iniciar la app se estará no registrado, por lo que se mostrará el botón de registro o inicio de sesión
            self.iniciar_label = ctk.CTkLabel(self.login_frame, text="Tiene una cuenta?")
            self.iniciar_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            self.iniciar_button = ctk.CTkButton(self.login_frame, text="Iniciar sesión", border_spacing=10, text_color="white", hover_color="seagreen", command=self.click_nav_iniciar_sesion)
            self.iniciar_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            # Botón para registrarse
            self.registro_label = ctk.CTkLabel(self.login_frame, text="No tiene una cuenta?")
            self.registro_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
            self.registro_button = ctk.CTkButton(self.login_frame, text="Registrarse", border_spacing=10, text_color="white", hover_color="seagreen", command=self.click_nav_registro)
            self.registro_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        for botoncito in factory.botones_navbar():
            print(botoncito)
            boton = ctk.CTkButton(self.nav_frame, text=botoncito["text"], corner_radius=0, border_spacing=10, text_color="white", fg_color="darkseagreen", hover_color="darkseagreen4", command=lambda: botoncito["command"](self.content_frame))
            boton.grid(row=2, column=0, sticky="ew")



    def color_selected_nav_button(self, boton):
        for button in self.nav_frame.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(fg_color="gray74", hover_color="gray44")
        boton.configure(fg_color="darkseagreen", hover_color="darkseagreen4")

    def click_nav_iniciar_sesion(self):
        self.color_selected_nav_button(self.iniciar_button)
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        # Aquí se debería abrir la ventana de inicio de sesión
        #self.vista_inicio_sesion = VistaInicioSesion(self.content_frame)
    
    def click_nav_registro(self):
        pass

    
    

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
