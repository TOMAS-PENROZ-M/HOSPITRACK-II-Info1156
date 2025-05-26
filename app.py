import customtkinter as ctk
from PIL import Image
import tkintermapview
from clases.Mapa import Mapa
from vistas.VistaMapa import VistaMapa

ctk.set_appearance_mode("Light")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (default), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hospitrack")
        self.geometry("1200x600")

        # Carpeta de imagenes
        self.img_folder = "imagenes"
        self.logo_imagen = ctk.CTkImage(Image.open(f"{self.img_folder}/logo.png"), size=(240, 80))

        # Columnas de la ventana principal
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Marco de navegación, a la izquierda --------------------------------------------------------------------------------------
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.grid(row=0, column=0, sticky="nswe")

        # Frame para el perfil o el inicio de sesión
        self.profile_frame = ctk.CTkFrame(self.nav_frame)
        self.profile_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.profile_frame.grid_rowconfigure(0, weight=1)

        # Al iniciar la app se estará no registrado, por lo que se mostrará el botón de registro o inicio de sesión
        self.iniciar_label = ctk.CTkLabel(self.profile_frame, text="Tiene una cuenta?")
        self.iniciar_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.iniciar_button = ctk.CTkButton(self.profile_frame, text="Iniciar sesión", border_spacing=10, text_color="white", hover_color="seagreen")
        self.iniciar_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Botón para registrarse
        self.registro_label = ctk.CTkLabel(self.profile_frame, text="No tiene una cuenta?")
        self.registro_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.registro_button = ctk.CTkButton(self.profile_frame, text="Registrarse", border_spacing=10, text_color="white", hover_color="seagreen")
        self.registro_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Boton para ir al mapa
        self.map_button = ctk.CTkButton(self.nav_frame, text="Mapa", corner_radius=0, border_spacing=10, text_color="white", fg_color="darkseagreen", hover_color="darkseagreen4", command=lambda: self.color_selected_nav_button(self.map_button))
        self.map_button.grid(row=2, column=0, sticky="ew")

        # Logo
        self.logo_label = ctk.CTkLabel(self.nav_frame, text="", image=self.logo_imagen)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)


        # Contenido principal, a la derecha --------------------------------------------------------------------------------------
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # Vista del mapa (por default al iniciar la app)
        self.vista_mapa = VistaMapa(self.content_frame)


    def color_selected_nav_button(self, boton):
        # Cambia el color del botón seleccionado y restablece los demás
        for button in self.nav_frame.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(fg_color="gray74", hover_color="gray44")
        boton.configure(fg_color="darkseagreen", hover_color="darkseagreen4")

    

app = App()
app.mainloop()