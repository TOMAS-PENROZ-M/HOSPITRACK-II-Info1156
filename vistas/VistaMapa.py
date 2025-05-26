import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.Mapa import Mapa
import customtkinter as ctk
import tkintermapview

class VistaMapa(ctk.CTkFrame):
    def __init__(self, master):    # Master será "content_frame" de la ventana principal, osea la parte derecha de la ventana
        super().__init__(master)
        
        # Frame superior con label explicativo
        self.top_frame = ctk.CTkFrame(self.master)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1)

        # Label titulo
        self.label_titulo = ctk.CTkLabel(self.top_frame, text="Bienvenido a Hospitrack", font=("Arial", 20))
        self.label_titulo.grid(row=0, column=0, padx=10, pady=10, sticky="ew")


        # Frame inferior
        self.bottom_frame = ctk.CTkFrame(self.master)
        self.bottom_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        self.bottom_frame.grid_columnconfigure(0, weight=3)
        self.bottom_frame.grid_columnconfigure(1, weight=2)
        self.bottom_frame.grid_rowconfigure(0, weight=1)

        # Frame del mapa
        self.map_frame = ctk.CTkFrame(self.bottom_frame)
        self.map_frame.grid(row=0, column=0, sticky="nwse")
        self.map_frame.grid_columnconfigure(0, weight=1)
        self.map_frame.grid_rowconfigure(0, weight=1)

        # Widget del mapa
        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, corner_radius=0)
        self.map_widget.set_position(-38.734547, -72.589724)
        self.map_widget.set_zoom(12)
        self.map_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        # Objeto mapa
        self.mapa = Mapa(self.map_widget)
        self.mapa.obtener_centros_salud()
        self.mapa.mostrar_centros()
        self.load_map_markers()

        # Frame donde irá la info del hospital seleccionado -------------------------------------------------------
        # El gran marco que contiene toda la información a la derecha del mapa
        self.right_info_frame = ctk.CTkScrollableFrame(self.bottom_frame, fg_color="#76B07D")
        self.right_info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Texto inicial, selecciona un centro de salud en el centro del frame
        self.hospital_name_label = ctk.CTkLabel(self.right_info_frame, text="Selecciona un centro de salud en el mapa", font=("Arial", 18, "bold"), anchor="center")
        self.hospital_name_label.pack(pady=(10, 5))
    
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
        for widget in self.right_info_frame.winfo_children():
            widget.destroy()
        if self.mapa.selected_marker:
            centro = self.mapa.selected_marker.centro_salud
            
            # Crea los widgets para mostrar la información del centro de salud
            # Nombre del centro de salud
            self.hospital_name_label = ctk.CTkLabel(self.right_info_frame, text=centro.nombre, font=("Arial", 18, "bold"), anchor="center")
            self.hospital_name_label.pack(pady=(10, 5))

            # Frame para secciones del hospital
            self.sections_frame = ctk.CTkFrame(self.right_info_frame)
            self.sections_frame.pack(pady=(10, 5), fill="x")

            self.sections_label = ctk.CTkLabel(self.sections_frame, text="Secciones del hospital", font=("Arial", 14, "bold"))
            self.sections_label.pack(pady=(5, 2))

            # Aquí se agregarán los botones de las secciones
            self.sections_buttons_frame = ctk.CTkFrame(self.right_info_frame, fg_color="#8CC6A2")
            self.sections_buttons_frame.pack(pady=(0, 5), fill="x")
            for seccion in centro.secciones:
                self.agregar_boton_seccion(seccion)
            
            # Fila de espera para sección seleccionada
            self.queue_info_frame = ctk.CTkFrame(self.right_info_frame, fg_color="#A5D6B5")
            self.queue_info_frame.pack(pady=(10, 5), fill="x")

            self.queue_label = ctk.CTkLabel(self.queue_info_frame, text="Seleccione una sección...", font=("Arial", 14, "bold"))
            self.queue_label.pack(pady=(5, 2))

            # Solicitudes de atención
            self.requests_frame = ctk.CTkFrame(self.right_info_frame, fg_color="#B8E0C7")
            self.requests_frame.pack(pady=(10, 5), fill="x")

            self.requests_label = ctk.CTkLabel(self.requests_frame, text="Solicitar atención", font=("Arial", 14, "bold"))
            self.requests_label.pack(pady=(5, 2))

            self.request_message_input = ctk.CTkTextbox(self.requests_frame, width=300, height=100)
            self.request_message_input.pack(pady=(5, 2), padx=10, fill="x")

            self.send_request_button = ctk.CTkButton(self.requests_frame, text="Enviar solicitud", command=self.on_send_request_click, border_spacing=10, text_color="white", hover_color="seagreen")
            self.send_request_button.pack(pady=(5, 2), padx=10, fill="x")
    
    def on_send_request_click(self):
        pass


    def agregar_boton_seccion(self, seccion):
        # Crear un botón para la sección
        button = ctk.CTkButton(self.sections_buttons_frame, text=seccion.nombre, command=lambda: self.on_section_button_click(seccion), border_spacing=10, text_color="white", hover_color="seagreen")
        button.pack(fill="x", padx=5, pady=5)

    def on_section_button_click(self, seccion):
        # Marca la seccion como seleccionada
        self.mapa.selected_seccion = seccion

        # Al hacer click en un botón de sección, actualizar la información de la fila de espera
        self.queue_label.configure(text=f"Fila de espera en {seccion.nombre}: {seccion.longitud_fila()}")
    