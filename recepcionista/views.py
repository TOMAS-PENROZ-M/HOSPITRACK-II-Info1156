# recepcionista/views.py
import os
import sys
# Asegura carpeta raíz en path para imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from recepcionista.db_bridge import DBBridge
from recepcionista.validation import FormValidator

# Estilo: igual que app.py, usando verde corporativo y texto negro
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")  # Paleta verde como en app.py

class VistaRecepcionista(ctk.CTk):
    """
    Vista del recepcionista que recibe solicitudes desde app.py.
    Permite aceptar, rechazar y dejar comentarios locales.
    Visualmente consistente con app.py.
    """
    def __init__(self):
        super().__init__()
        self.title("Recepcionista - Hospitrack")
        self.geometry("1000x650")
        self.configure(fg_color="#ffffff")  # Fondo blanco para toda la ventana

        # Dependencias
        self.bridge = DBBridge()
        self.validador = FormValidator()
        self.comentarios = {}

        self._construir_vista()

    def _construir_vista(self):
        self._limpiar_ventana()

        # Encabezado con logo y título
        header = ctk.CTkFrame(self, fg_color="#28A745", corner_radius=0)
        header.pack(fill="x")
        # Logo a la izquierda
        logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'logo.png'))
        if os.path.exists(logo_path):
            raw = Image.open(logo_path)
            ratio = raw.width / raw.height
            new_h = 50
            new_w = int(new_h * ratio)
            img = ctk.CTkImage(raw.resize((new_w, new_h), Image.LANCZOS))
            lbl_logo = ctk.CTkLabel(header, image=img, text="", fg_color="#28A745")
            lbl_logo.pack(side="left", padx=20, pady=10)
        # Título centrado
        lbl_title = ctk.CTkLabel(header, text="Solicitudes Pendientes", font=("Arial", 20, "bold"), text_color="#000000", fg_color="#28A745")
        lbl_title.pack(side="left", pady=10)

        # Contenedor principal de solicitudes
        cont = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=8)
        cont.pack(fill="both", expand=True, padx=20, pady=20)

        # ScrollableFrame para solicitudes
        self.scroll = ctk.CTkScrollableFrame(cont, fg_color="#ffffff", scrollbar_button_color="#28A745")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Footer con botones
        footer = ctk.CTkFrame(self, fg_color="#ffffff")
        footer.pack(fill="x", padx=20, pady=(0,20))
        btn_refresh = ctk.CTkButton(footer, text="Refrescar", fg_color="#28A745", hover_color="#218838", width=100, command=self._mostrar_solicitudes)
        btn_refresh.pack(side="left", padx=(0,10))
        btn_exit = ctk.CTkButton(footer, text="Salir", fg_color="#dc3545", hover_color="#c82333", width=100, command=self._cerrar)
        btn_exit.pack(side="right")

        # Carga inicial de solicitudes
        self._mostrar_solicitudes()

    def _mostrar_solicitudes(self):
        # Limpia lista
        for w in self.scroll.winfo_children():
            w.destroy()

        pendientes = self.bridge.obtener_solicitudes_pendientes()
        if not pendientes:
            ctk.CTkLabel(self.scroll, text="No hay solicitudes pendientes.", font=("Arial",16), text_color="#555555").pack(pady=30)
            return

        # Muestra cada solicitud
        for sol in pendientes:
            sol_id = getattr(sol, sol.__mapper__.primary_key[0].name)
            frame = ctk.CTkFrame(self.scroll, fg_color="#ffffff", corner_radius=6)
            frame.pack(fill="x", pady=5, padx=10)
            # Encabezado de la solicitud
            header_text = f"#{sol_id} {sol.nombre} {sol.apellido} | RUT: {sol.rut}"
            ctk.CTkLabel(frame, text=header_text, font=("Arial",14,"bold"), text_color="#000000").grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(5,0))
            # Motivo
            ctk.CTkLabel(frame, text=f"Motivo: {sol.motivo}", font=("Arial",12), text_color="#000000").grid(row=1, column=0, columnspan=3, sticky="w", padx=10)
            # Comentario
            ctk.CTkLabel(frame, text="Comentario:", font=("Arial",12), text_color="#000000").grid(row=2, column=0, sticky="nw", padx=10, pady=(5,0))
            txt = ctk.CTkTextbox(frame, height=4, fg_color="#f5f5f5")
            txt.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=(5,0))
            if sol_id in self.comentarios:
                txt.insert("1.0", self.comentarios[sol_id])
            # Botones acción
            ctk.CTkButton(frame, text="Aceptar", fg_color="#28A745", hover_color="#218838", width=80,
                          command=lambda s=sol_id,t=txt: self._procesar(s,t,True)).grid(row=0, column=3, padx=5)
            ctk.CTkButton(frame, text="Rechazar", fg_color="#dc3545", hover_color="#c82333", width=80,
                          command=lambda s=sol_id,t=txt: self._procesar(s,t,False)).grid(row=1, column=3, padx=5)

    def _procesar(self, sol_id, textbox, aceptar):
        comentario = textbox.get("1.0","end").strip()
        self.comentarios[sol_id] = comentario
        ok = self.bridge.aceptar_solicitud(sol_id) if aceptar else self.bridge.rechazar_solicitud(sol_id)
        if ok:
            messagebox.showinfo("Éxito", f"Solicitud {'aceptada' if aceptar else 'rechazada'}.")
        else:
            messagebox.showwarning("Error","No se encontró la solicitud.")
        self._mostrar_solicitudes()

    def _limpiar_ventana(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _cerrar(self):
        self.bridge.cerrar()
        self.destroy()

if __name__ == '__main__':
    app = VistaRecepcionista()
    app.mainloop()