import customtkinter as ctk
from PIL import Image
import tkintermapview
from clases.Mapa import Mapa

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

        # Frame superior con label explicativo
        self.top_frame = ctk.CTkFrame(self.content_frame)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1)

        # Label titulo
        self.label_titulo = ctk.CTkLabel(self.top_frame, text="Bienvenido a Hospitrack", font=("Arial", 20))
        self.label_titulo.grid(row=0, column=0, padx=10, pady=10, sticky="ew")


        # Frame inferior
        self.bottom_frame = ctk.CTkFrame(self.content_frame)
        self.bottom_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        self.bottom_frame.grid_columnconfigure(0, weight=3)
        self.bottom_frame.grid_columnconfigure(1, weight=2)
        self.bottom_frame.grid_rowconfigure(0, weight=1)

        # Frame del mapa
        self.map_frame = ctk.CTkFrame(self.bottom_frame)
        self.map_frame.grid(row=0, column=0, sticky="nwse")
        self.map_frame.grid_columnconfigure(0, weight=1)
        self.map_frame.grid_rowconfigure(0, weight=1)

        # Mapa
        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, corner_radius=0)
        self.map_widget.set_position(-38.734547, -72.589724)
        self.map_widget.set_zoom(12)
        self.map_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        # Objeto mapa
        self.mapa = Mapa(self.map_widget)
        self.mapa.obtener_centros_salud()
        self.mapa.mostrar_centros()
        self.load_map_markers()

        # frame donde irá la info del hospital seleccionado -------------------------------------------------------
        # El gran marco que contiene toda la información a la derecha del mapa
        self.right_info_frame = ctk.CTkScrollableFrame(self.bottom_frame, fg_color="#76B07D")
        self.right_info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 🌟 Nombre del hospital seleccionado
        self.hospital_name_label = ctk.CTkLabel(self.right_info_frame, text="Nombre del centro de salud", font=("Arial", 18, "bold"), anchor="center")
        self.hospital_name_label.pack(pady=(10, 5))

        # 🧱 Frame para secciones
        self.sections_frame = ctk.CTkFrame(self.right_info_frame, fg_color="#8CC6A2")
        self.sections_frame.pack(fill="x", padx=10, pady=(5, 10))

        self.sections_label = ctk.CTkLabel(self.sections_frame, text="Secciones del hospital", font=("Arial", 14, "bold"))
        self.sections_label.pack(pady=(5, 2))

        # Aquí van dinámicamente los botones o etiquetas de cada sección
        self.sections_buttons_frame = ctk.CTkFrame(self.sections_frame, fg_color="transparent")
        self.sections_buttons_frame.pack(pady=(0, 5), fill="x")

        # 🕰️ Fila de espera para sección seleccionada
        self.queue_info_frame = ctk.CTkFrame(self.right_info_frame, fg_color="#A5D6B5")
        self.queue_info_frame.pack(fill="x", padx=10, pady=(5, 10))

        self.queue_label = ctk.CTkLabel(self.queue_info_frame, text="Fila de espera en...", font=("Arial", 14, "bold"))
        self.queue_label.pack(pady=(5, 2))

        # 📝 Formulario de solicitud
        self.form_frame = ctk.CTkFrame(self.right_info_frame, fg_color="#C7E7D1")
        self.form_frame.pack(fill="x", padx=10, pady=(5, 10))

        self.form_label = ctk.CTkLabel(self.form_frame, text="Enviar solicitud", font=("Arial", 14, "bold"))
        self.form_label.pack(pady=(5, 2))

        self.message_entry = ctk.CTkTextbox(self.form_frame, height=60)
        self.message_entry.pack(fill="x", padx=5, pady=5)

        self.send_button = ctk.CTkButton(self.form_frame, text="Enviar solicitud")
        self.send_button.pack(pady=(5, 10))
    

    def load_map_markers(self):
        # Cargar los marcadores en el mapa
        for centro_marker in self.mapa.markers:
            visual_marker = self.map_widget.set_marker(centro_marker.centro_salud.latitud, centro_marker.centro_salud.longitud, text=centro_marker.centro_salud.nombre)
            visual_marker._objeto_marker = centro_marker    # Vincula los datos del marcador con el marcador de la interfaz
            visual_marker.command = lambda marker=visual_marker: self.on_marker_click(marker._objeto_marker)  # Asigna la función de clic al marcador

    
    def on_marker_click(self, clicked_marker):
        self.mapa.selected_marker = clicked_marker
        self.map_widget.set_position(clicked_marker.centro_salud.latitud, clicked_marker.centro_salud.longitud)
        # Carga la información del centro de salud seleccionado
        self.actualizar_info_mapa()

    def actualizar_info_mapa(self):
        if self.mapa.selected_marker:
            centro = self.mapa.selected_marker.centro_salud
            self.hospital_name_label.configure(text=centro.nombre)
            # Agregar botones de secciones
            self.secciones = centro.secciones
            for seccion in self.secciones:
                self.agregar_boton_seccion(seccion)
            # Actualizar la fila de espera
    
    def agregar_boton_seccion(self, seccion):
        # Crear un botón para la sección
        button = ctk.CTkButton(self.sections_buttons_frame, text=seccion.nombre, command=lambda: self.on_section_button_click(seccion), border_spacing=10, text_color="white", hover_color="seagreen")
        button.pack(fill="x", padx=5, pady=5)

    def on_section_button_click(self, seccion):
        # Marca la seccion como seleccionada
        self.mapa.selected_seccion = seccion

        # Al hacer click en un botón de sección, actualizar la información de la fila de espera
        self.queue_label.configure(text=f"Fila de espera en {seccion.nombre}: {seccion.longitud_fila()}")

    def color_selected_nav_button(self, boton):
        # Cambia el color del botón seleccionado y restablece los demás
        for button in self.nav_frame.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(fg_color="gray74", hover_color="gray44")
        boton.configure(fg_color="darkseagreen", hover_color="darkseagreen4")

    

app = App()
app.mainloop()