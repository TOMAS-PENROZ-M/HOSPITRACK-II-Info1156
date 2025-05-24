import os
import sys
# Agrega la carpeta raíz del proyecto al path para importar módulos raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy import asc
from database import SessionLocal
from models import SolicitudDB
from recepcionista.auto_logout import AutoLogout
from recepcionista.validation import FormValidator
from recepcionista.management import GestorSolicitudesPrueba
from recepcionista.categorization import Categorizador

class VistaRecepcionista(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Recepcionista - Hospitrack")
        self.geometry("900x600")
        self.sesion = SessionLocal()
        self.validador = FormValidator()
        self.categorizador = Categorizador()
        self._construir_vista_principal()

    def _construir_vista_principal(self):
        self._limpiar_ventana()
        # Configura auto logout
        self.auto_logout = AutoLogout(timeout_sec=300, on_logout=self._cerrar_sesion)
        self.bind_all("<Any-KeyPress>", lambda e: self.auto_logout.reset_timer())

        self.marco_principal = ctk.CTkFrame(self)
        self.marco_principal.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(self.marco_principal, text="Panel del Recepcionista", font=("Arial", 24)).pack(pady=10)
        ctk.CTkButton(self.marco_principal, text="Cerrar Sesión", command=self._cerrar_sesion).pack(pady=5)

        self._construir_seccion_solicitudes()
        self._construir_formulario()

    def _construir_seccion_solicitudes(self):
        self.marco_solicitudes = ctk.CTkFrame(self.marco_principal)
        self.marco_solicitudes.pack(side="left", expand=True, fill="both", padx=(0,10))

        ctk.CTkLabel(self.marco_solicitudes, text="Solicitudes Recibidas", font=("Arial", 18)).pack(pady=5)
        ctk.CTkButton(self.marco_solicitudes, text="Refrescar", command=self._refrescar_solicitudes).pack(pady=5)

        self.lista_solicitudes = ctk.CTkScrollableFrame(self.marco_solicitudes, width=400, height=400)
        self.lista_solicitudes.pack(pady=5, padx=5)

        self._refrescar_solicitudes()

    def _construir_formulario(self):
        self.marco_formulario = ctk.CTkFrame(self.marco_principal)
        self.marco_formulario.pack(side="right", expand=True, fill="both", padx=(10,0))

        ctk.CTkLabel(self.marco_formulario, text="Nueva Solicitud (Prueba)", font=("Arial", 18)).pack(pady=5)
        self.entrada_titulo = ctk.CTkEntry(self.marco_formulario, placeholder_text="Título")
        self.entrada_titulo.pack(pady=5)
        self.texto_descripcion = ctk.CTkTextbox(self.marco_formulario, height=10)
        self.texto_descripcion.pack(pady=5)

        ctk.CTkButton(self.marco_formulario, text="Agregar", command=self._agregar_solicitud).pack(pady=5)
        ctk.CTkButton(self.marco_formulario, text="Asignar Pendientes", command=self._asignar_pruebas).pack(pady=5)

    def _refrescar_solicitudes(self):
        # Limpia lista previa
        for w in self.lista_solicitudes.winfo_children():
            w.destroy()
        # Obtiene primer key dinamicamente
        pk = SolicitudDB.__mapper__.primary_key[0]
        solicitudes = self.sesion.query(SolicitudDB).order_by(asc(pk)).all()

        for sol in solicitudes:
            sol_id = getattr(sol, pk.name)
            prioridad = self.categorizador.categorizar(sol).value
            texto = f"#{sol_id} {sol.titulo} - {sol.estado} ({prioridad})"
            ctk.CTkLabel(self.lista_solicitudes, text=texto, anchor="w").pack(fill="x", pady=2, padx=5)

    def _agregar_solicitud(self):
        titulo = self.entrada_titulo.get().strip()
        descripcion = self.texto_descripcion.get("1.0", "end").strip()
        if not self.validador.validate_and_show({"titulo": titulo, "descripcion": descripcion}):
            return
        nueva = SolicitudDB(titulo=titulo, descripcion=descripcion, estado="pendiente")
        self.sesion.add(nueva)
        self.sesion.commit()
        messagebox.showinfo("Éxito", "Solicitud agregada en modo de prueba")
        self.entrada_titulo.delete(0, "end")
        self.texto_descripcion.delete("1.0", "end")
        self._refrescar_solicitudes()

    def _asignar_pruebas(self):
        gestor = GestorSolicitudesPrueba()
        gestor.asignar_pruebas()
        messagebox.showinfo("Asignado", "Solicitudes pendientes actualizadas")
        self._refrescar_solicitudes()

    def _cerrar_sesion(self):
        # Detiene auto logout
        if hasattr(self, 'auto_logout'):
            self.auto_logout.stop()
        self._construir_vista_principal()

    def _limpiar_ventana(self):
        for w in self.winfo_children():
            w.destroy()

if __name__ == "__main__":
    app = VistaRecepcionista()
    app.mainloop()
