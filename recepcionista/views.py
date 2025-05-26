# recepcionista/views.py
import os
import sys
# Asegura que la carpeta raíz del proyecto esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from typing import Any
import traceback

# Import correcto desde models.py
from recepcionista.models_recep import (
    SolicitudFactory,
    RecepcionistaFacade,
    SolicitudRepository,
    Observador
)
from recepcionista.validation import FormValidator


class VistaSolicitudesObserver(Observador):
    """
    Observador que recibe eventos del repositorio para refrescar la vista.
    """
    def __init__(self, callback: Any):
        self.callback = callback

    def actualizar(self, evento: str, datos: Any) -> None:
        # En cualquier cambio, solicitamos refrescar la lista
        self.callback()


class VistaRecepcionista(ctk.CTk):
    """
    Interfaz principal del recepcionista.
    Usa Façade, Observer, Command y Factory según lo definido en models.py.
    """
    def __init__(self):
        super().__init__()
        self.title("Sistema Recepcionista - Hospitrack")
        self.geometry("900x600")

        # Dependencias
        self.facade = RecepcionistaFacade()
        self.validador = FormValidator()

        # Observer para actualizaciones de solicitudes
        self.obs = VistaSolicitudesObserver(self._refrescar_solicitudes)
        SolicitudRepository().registrar_observador(self.obs)

        self._construir_widget_principal()

    def _construir_widget_principal(self) -> None:
        """
        Construye los widgets principales.
        """
        self._limpiar_ventana()

        # Marco principal
        marco = ctk.CTkFrame(self)
        marco.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(marco, text="Panel del Recepcionista", font=("Arial", 24)).pack(pady=(0, 10))

        # Sección de solicitudes
        sub_frame = ctk.CTkFrame(marco)
        sub_frame.pack(side="left", expand=True, fill="both", padx=(0,5))
        ctk.CTkLabel(sub_frame, text="Solicitudes", font=("Arial", 18)).pack(pady=5)
        ctk.CTkButton(sub_frame, text="Refrescar", command=self._refrescar_solicitudes).pack(pady=5)
        self.lista_frame = ctk.CTkScrollableFrame(sub_frame, width=400, height=400)
        self.lista_frame.pack(pady=5, padx=5)
        self._refrescar_solicitudes()

        # Sección de formulario
        form_frame = ctk.CTkFrame(marco)
        form_frame.pack(side="right", expand=True, fill="both", padx=(5,0))
        ctk.CTkLabel(form_frame, text="Agregar Nueva Solicitud", font=("Arial", 18)).pack(pady=5)
        self.entrada_titulo = ctk.CTkEntry(form_frame, placeholder_text="Título")
        self.entrada_titulo.pack(pady=5)
        self.entrada_descripcion = ctk.CTkTextbox(form_frame, height=10)
        self.entrada_descripcion.pack(pady=5)
        ctk.CTkButton(form_frame, text="Agregar Normal", command=self._cmd_agregar_normal).pack(pady=(5,0))
        ctk.CTkButton(form_frame, text="Agregar Urgente", fg_color="red", command=self._cmd_agregar_urgente).pack(pady=5)

        # Botón salir
        ctk.CTkButton(marco, text="Salir", command=self._cerrar_aplicacion).pack(side="bottom", pady=10)

    def _refrescar_solicitudes(self) -> None:
        """
        Elimina los widgets actuales y refresca la lista de solicitudes.
        """
        for w in self.lista_frame.winfo_children():
            w.destroy()

        solicitudes = self.facade.obtener_solicitudes()
        for sol in solicitudes:
            texto = f"#{sol.id} {sol.titulo} - {sol.estado}"
            prioridad = " (Urgente)" if sol.es_urgente else ""
            label = ctk.CTkLabel(self.lista_frame, text=texto + prioridad, anchor="w")
            label.pack(fill="x", pady=2, padx=5)

    def _cmd_agregar_normal(self) -> None:
        self._ejecutar_agregar(False)

    def _cmd_agregar_urgente(self) -> None:
        self._ejecutar_agregar(True)

    def _ejecutar_agregar(self, urgente: bool) -> None:
        """
        Valida el formulario, crea la solicitud y refresca la lista. Maneja errores.
        """
        try:
            titulo = self.entrada_titulo.get().strip()
            descripcion = self.entrada_descripcion.get("1.0", "end").strip()
            if not self.validador.validate_and_show({"titulo": titulo, "descripcion": descripcion}):
                return

            # Crear solicitud
            sol = (
                SolicitudFactory.crear_solicitud_urgente(titulo, descripcion)
                if urgente else
                SolicitudFactory.crear_solicitud_normal(titulo, descripcion)
            )

            # Agregar vía Facade
            self.facade.agregar_solicitud(sol)

            # Refrescar lista
            self._refrescar_solicitudes()

            # Limpiar formulario
            self.entrada_titulo.delete(0, "end")
            self.entrada_descripcion.delete("1.0", "end")

        except Exception as e:
            # Mostrar error al usuario y log para debugging
            message = f"Error al agregar solicitud: {e}"
            print(traceback.format_exc())
            ctk.messagebox.showerror("Error Interno", message)

    def _cerrar_aplicacion(self) -> None:
        """
        Cierra la aplicación.
        """
        self.destroy()

    def _limpiar_ventana(self) -> None:
        """
        Elimina todos los widgets de la ventana.
        """
        for w in self.winfo_children():
            w.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = VistaRecepcionista()
    app.mainloop()
