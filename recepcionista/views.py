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
    Vista del recepcionista que recibe entradas de fila de espera desde app.py.
    Permite aceptar, rechazar y dejar comentarios locales, con estilo coherente.
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

        # Construcción de la interfaz
        self._construir_vista()

    def _construir_vista(self):
        self._limpiar_ventana()

        # Encabezado con logo y título
        header = ctk.CTkFrame(self, fg_color="#28A745", corner_radius=0)
        header.pack(fill="x")
        # Logo a la izquierda
        logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'logo.png'))
        if os.path.exists(logo_path):
            img_raw = Image.open(logo_path)
            ratio = img_raw.width / img_raw.height
            new_h = 50
            new_w = int(new_h * ratio)
            img_ctk = ctk.CTkImage(img_raw.resize((new_w, new_h), Image.LANCZOS))
            ctk.CTkLabel(header, image=img_ctk, text="", fg_color="#28A745").pack(side="left", padx=20, pady=10)
        # Título centrado
        ctk.CTkLabel(
            header,
            text="Solicitudes en Espera",
            font=("Arial", 20, "bold"),
            text_color="#000000",
            fg_color="#28A745"
        ).pack(side="left", pady=10)

        # Contenedor principal de solicitudes
        cont = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=8)
        cont.pack(fill="both", expand=True, padx=20, pady=20)

        # ScrollableFrame para solicitudes
        self.scroll = ctk.CTkScrollableFrame(cont, fg_color="#ffffff", scrollbar_button_color="#28A745")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Footer con botones
        footer = ctk.CTkFrame(self, fg_color="#ffffff")
        footer.pack(fill="x", padx=20, pady=(0,20))
        ctk.CTkButton(
            footer,
            text="Refrescar",
            fg_color="#28A745",
            hover_color="#218838",
            width=100,
            command=self._mostrar_solicitudes
        ).pack(side="left", padx=(0,10))
        ctk.CTkButton(
            footer,
            text="Salir",
            fg_color="#dc3545",
            hover_color="#c82333",
            width=100,
            command=self._cerrar
        ).pack(side="right")

        # Carga inicial de solicitudes
        self._mostrar_solicitudes()

    def _mostrar_solicitudes(self):
        # Limpia lista
        for widget in self.scroll.winfo_children():
            widget.destroy()

        # Obtener filas de espera
        entradas = self.bridge.listar_espera()
        if not entradas:
            ctk.CTkLabel(
                self.scroll,
                text="No hay entradas en la fila de espera.",
                font=("Arial", 16),
                text_color="#555555"
            ).pack(pady=30)
            return

        # Muestra cada entrada
        for entrada in entradas:
            entrada_id = getattr(entrada, entrada.__mapper__.primary_key[0].name)
            frame = ctk.CTkFrame(self.scroll, fg_color="#ffffff", corner_radius=6)
            frame.pack(fill="x", pady=5, padx=10)

            # Datos de la fila de espera
            ctk.CTkLabel(
                frame,
                text=f"#{entrada_id} RUT: {entrada.RUT}",
                font=("Arial", 14, "bold"),
                text_color="#000000"
            ).grid(row=0, column=0, sticky="w", padx=10, pady=(5,0))
            ctk.CTkLabel(
                frame,
                text=f"Prioridad: {entrada.Prioridad}  |  Hora: {entrada.HoraRegistro}",
                font=("Arial", 12),
                text_color="#000000"
            ).grid(row=1, column=0, sticky="w", padx=10)

            # Comentario local
            ctk.CTkLabel(
                frame,
                text="Comentario:",
                font=("Arial", 12),
                text_color="#000000"
            ).grid(row=2, column=0, sticky="nw", padx=10, pady=(5,0))
            txt = ctk.CTkTextbox(frame, height=4, fg_color="#f5f5f5")
            txt.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=(5,0))
            if entrada_id in self.comentarios:
                txt.insert("1.0", self.comentarios[entrada_id])

            # Botones Aceptar / Rechazar
            ctk.CTkButton(
                frame,
                text="Aceptar",
                fg_color="#28A745",
                hover_color="#218838",
                width=80,
                command=lambda i=entrada_id, t=txt: self._procesar(i, t, True)
            ).grid(row=0, column=3, padx=5)
            ctk.CTkButton(
                frame,
                text="Rechazar",
                fg_color="#dc3545",
                hover_color="#c82333",
                width=80,
                command=lambda i=entrada_id, t=txt: self._procesar(i, t, False)
            ).grid(row=1, column=3, padx=5)

    def _procesar(self, entrada_id, textbox, aceptar):
        comentario = textbox.get("1.0", "end").strip()
        self.comentarios[entrada_id] = comentario

        if aceptar:
            ok = self.bridge.aceptar_entrada(entrada_id)
            acción = "atendida"
        else:
            ok = self.bridge.rechazar_entrada(entrada_id)
            acción = "rechazada"

        if ok:
            messagebox.showinfo("Éxito", f"Entrada {acción}.")
        else:
            messagebox.showwarning("Error", "No se encontró la entrada.")

        self._mostrar_solicitudes()

    def _limpiar_ventana(self):
        """
        Elimina todos los widgets de la ventana principal.
        """
        for widget in self.winfo_children():
            widget.destroy()

    def _cerrar(self):
        """
        Cierra la sesión y destruye la ventana.
        """
        self.bridge.cerrar()
        self.destroy()


if __name__ == '__main__':
    app = VistaRecepcionista()
    app.mainloop()
