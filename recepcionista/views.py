# recepcionista/views.py

"""
VistaRecepcionista con patrones modularizados:
- Strategy (OrdenEstrategia) desde recepcionista.patrones.strategy
- Decorator/Exportador desde recepcionista.patrones.exportador
- Observer desde recepcionista.patrones.observer
- Principios SOLID: SRP, OCP, LSP, ISP, DIP
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from datetime import datetime

from recepcionista.db_bridge import DBBridge
from recepcionista.validation import FormValidator
from recepcionista.patrones.strategy import OrdenAscendente, OrdenDescendente
from recepcionista.patrones.exportador import ExportadorPDF
from recepcionista.patrones.observer import Observer

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class VistaRecepcionista(ctk.CTkFrame, Observer):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#ffffff")
        # DIP: uso de abstracciones
        self.bridge = DBBridge()
        self.validador = FormValidator()
        self.comentarios = {}
        self.vista_actual = 'pendientes'
        self.filtro_busqueda = ''
        # Strategy
        self.estrategia_orden = OrdenDescendente()
        self._construir_vista()

    def _construir_vista(self):
        # SRP: construcción UI separada de lógica
        self._limpiar_ventana()

        # Navegación interna
        nav = ctk.CTkFrame(self, fg_color="#f0f0f0")
        nav.pack(fill="x", pady=(0,5))
        ctk.CTkButton(nav, text="Pendientes", width=120,
                      command=lambda: self._cambiar_vista('pendientes')).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(nav, text="Historial", width=120,
                      command=lambda: self._cambiar_vista('historial')).pack(side="left", padx=10, pady=5)

        # Área principal scroll
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#ffffff", scrollbar_button_color="#28A745")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Footer con acciones generales
        footer = ctk.CTkFrame(self, fg_color="#ffffff")
        footer.pack(fill="x", padx=20, pady=(0,20))
        ctk.CTkButton(footer, text="Refresh", fg_color="#28A745", hover_color="#218838",
                      width=100, command=self._refrescar).pack(side="left")
        ctk.CTkButton(footer, text="Exportar PDF", fg_color="#007bff", hover_color="#0056b3",
                      width=120, command=self._exportar_historial_pdf).pack(side="left", padx=(10, 0))
        ctk.CTkButton(footer, text="Cerrar", fg_color="#dc3545", hover_color="#c82333",
                      width=100, command=self._cerrar).pack(side="right")

        self._cargar_vista()

    def _cambiar_vista(self, vista):
        if vista == self.vista_actual:
            return
        self.vista_actual = vista
        self._cargar_vista()

    def _cargar_vista(self):
        # Limpiar contenido previo
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        # Mostrar según estado
        if self.vista_actual == 'pendientes':
            self._mostrar_pendientes()
        else:
            self._dibujar_filtros_historial()
            self._mostrar_historial()

    def _dibujar_filtros_historial(self):
        filtro_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#ffffff")
        filtro_frame.pack(fill="x", pady=(5, 10), padx=10)

        ctk.CTkLabel(filtro_frame, text="Ordenar por fecha:", font=("Arial",12), text_color="#000").pack(side="left", padx=(0,5))
        self.orden_dropdown = ctk.CTkOptionMenu(
            filtro_frame,
            values=["Descendente (más reciente)", "Ascendente (más antiguo)"],
            command=self._actualizar_orden_fecha
        )
        self.orden_dropdown.pack(side="left", padx=5)
        self.orden_dropdown.set("Descendente (más reciente)")

        ctk.CTkLabel(filtro_frame, text="Buscar por RUT o ID:", font=("Arial",12), text_color="#000").pack(side="left", padx=(10,5))
        self.busqueda_entry = ctk.CTkEntry(filtro_frame, placeholder_text="RUT o ID", width=150)
        self.busqueda_entry.pack(side="left", padx=5)

        ctk.CTkButton(filtro_frame, text="Buscar", fg_color="#007bff", hover_color="#0056b3",
                      command=self._aplicar_filtros).pack(side="left", padx=5)
        ctk.CTkButton(filtro_frame, text="Limpiar filtros", fg_color="#6c757d", hover_color="#5a6268",
                      command=self._limpiar_filtros).pack(side="left", padx=5)

    def _actualizar_orden_fecha(self, value):
        # Strategy: cambiar estrategia a voluntad
        if 'Ascendente' in value:
            self.estrategia_orden = OrdenAscendente()
        else:
            self.estrategia_orden = OrdenDescendente()
        self._mostrar_historial()

    def _aplicar_filtros(self):
        self.filtro_busqueda = self.busqueda_entry.get().strip().lower()
        self._mostrar_historial()

    def _limpiar_filtros(self):
        self.filtro_busqueda = ''
        self.estrategia_orden = OrdenDescendente()
        self.orden_dropdown.set("Descendente (más reciente)")
        self.busqueda_entry.delete(0, 'end')
        self._mostrar_historial()

    def _mostrar_pendientes(self):
        solicitudes = self.bridge.listar_solicitudes()
        if not solicitudes:
            ctk.CTkLabel(self.scroll_frame, text="No hay solicitudes pendientes.", font=("Arial",16), text_color="#555").pack(pady=30)
            return
        for sol in solicitudes:
            sol_id = getattr(sol, sol.__mapper__.primary_key[0].name)
            frame = ctk.CTkFrame(self.scroll_frame, fg_color="#fff", corner_radius=6)
            frame.pack(fill="x", pady=5, padx=10)
            nombre = getattr(sol, 'Nombre', '')
            apellido = getattr(sol, 'Apellido', '')
            rut = getattr(sol, 'RUT', '')
            hora = getattr(sol, 'HoraSolicitud', '')
            estado = getattr(sol, 'Estado', '')
            ctk.CTkLabel(frame, text=f"#{sol_id} {nombre} {apellido} | RUT: {rut}", font=("Arial",14,"bold"), text_color="#000").grid(row=0, column=0, columnspan=3, sticky="w", padx=10)
            ctk.CTkLabel(frame, text=f"Motivo: {getattr(sol,'Mensaje','')}", font=("Arial",12), text_color="#000").grid(row=1, column=0, columnspan=3, sticky="w", padx=10)
            ctk.CTkLabel(frame, text=f"Hora: {hora}  |  Estado: {estado}", font=("Arial",12), text_color="#000").grid(row=2, column=0, columnspan=3, sticky="w", padx=10)
            ctk.CTkLabel(frame, text="Comentario:", font=("Arial",12), text_color="#000").grid(row=3, column=0, sticky="nw", padx=10)
            txt = ctk.CTkTextbox(frame, height=4, fg_color="#f5f5f5")
            txt.grid(row=3, column=1, columnspan=2, sticky="we", padx=5)
            if sol_id in self.comentarios:
                txt.insert("1.0", self.comentarios[sol_id])
            ctk.CTkButton(frame, text="Aceptar", fg_color="#28A745", hover_color="#218838", width=80,
                          command=lambda i=sol_id, t=txt: self._procesar(i, t, True)).grid(row=0, column=3, padx=5)
            ctk.CTkButton(frame, text="Rechazar", fg_color="#dc3545", hover_color="#c82333", width=80,
                          command=lambda i=sol_id, t=txt: self._procesar(i, t, False)).grid(row=1, column=3, padx=5)

    def _mostrar_historial(self):
        registros = self.bridge.obtener_historial()
        if self.filtro_busqueda:
            registros = [r for r in registros if self.filtro_busqueda in (str(r.IdRegistro) + (r.RUT or '')).lower()]
        registros = self.estrategia_orden.ordenar(registros)
        if not registros:
            ctk.CTkLabel(self.scroll_frame, text="No hay historial de atenciones.", font=("Arial",16), text_color="#555").pack(pady=30)
            return
        header = ctk.CTkFrame(self.scroll_frame, fg_color="#fff")
        header.pack(fill="x", pady=(5,0), padx=10)
        for idx, t in enumerate(["ID","RUT","Sección","Prioridad","Estado","Comentario","Fecha"]):
            ctk.CTkLabel(header, text=t, font=("Arial",12,"bold"), text_color="#000").grid(row=0, column=idx, padx=5)
        for rec in registros:
            row = ctk.CTkFrame(self.scroll_frame, fg_color="#f9f9f9")
            row.pack(fill="x", pady=2, padx=10)
            valores = [
                rec.IdRegistro,
                rec.RUT or '',
                rec.IdSeccion,
                rec.Prioridad or '',
                rec.EstadoFinal or '',
                rec.Comentario or '',
                rec.FechaResolucion.strftime("%Y-%m-%d") if rec.FechaResolucion else ''
            ]
            for idx, v in enumerate(valores):
                ctk.CTkLabel(row, text=str(v), font=("Arial",12), text_color="#000").grid(row=0, column=idx, padx=5)

    def _exportar_historial_pdf(self):
        registros = self.bridge.obtener_historial()
        if not registros:
            messagebox.showinfo("Exportar PDF", "No hay registros para exportar.")
            return
        exportador = ExportadorPDF("historial_atenciones.pdf")
        exportador.exportar(registros)
        messagebox.showinfo("Exportar PDF", "PDF guardado correctamente.")

    def _refrescar(self):
        self._cargar_vista()

    def _procesar(self, sol_id, textbox, aceptar):
        comentario = textbox.get("1.0", "end").strip()
        self.comentarios[sol_id] = comentario
        if aceptar:
            ok = self.bridge.aceptar_solicitud(sol_id, comentario)
            accion = "aceptada"
        else:
            ok = self.bridge.rechazar_solicitud(sol_id, comentario)
            accion = "rechazada"
        if ok:
            messagebox.showinfo("Éxito", f"Solicitud {accion}.")
        else:
            messagebox.showwarning("Error", "No se encontró la solicitud.")
        self._cargar_vista()

    def actualizar(self, evento):
        if evento == 'refrescar':
            self._refrescar()

    def _limpiar_ventana(self):
        for w in self.winfo_children():
            w.destroy()

    def _cerrar(self):
        self.bridge.cerrar()
        self.grid_forget()
