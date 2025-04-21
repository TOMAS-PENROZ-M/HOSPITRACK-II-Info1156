import customtkinter as ctk
from PIL import Image

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
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Marco de navegación, a la izquierda
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.grid(row=0, column=0, sticky="nswe")

        # Logo
        self.logo_label = ctk.CTkLabel(self.nav_frame, text="", image=self.logo_imagen)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)

    def on_button_click(self):
        print("Button clicked!")

app = App()
app.mainloop()