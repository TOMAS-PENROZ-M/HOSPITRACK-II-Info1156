# recepcionista/views.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recepcionista.db_interfaces import IRequestRepository
from recepcionista.db_bridge import DBBridge
from recepcionista.patrones.exportador import ExportadorCSV, ExportadorPDF
from recepcionista.patrones.strategy import OrdenAscendente, OrdenDescendente
from recepcionista.patrones.observer import Subject, Observer

class VistaRecepcionista(ctk.CTkFrame, Observer):
    def __init__(self, master, repo: IRequestRepository):
        super().__init__(master)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")
        self.repo = repo
        self.comentarios = {}
        self.vista_actual = 'Pendientes'
        # Filtros: fecha_desde, fecha_hasta, seccion, tipo, busqueda
        self.filtros = {'fecha_desde': None, 'fecha_hasta': None, 'seccion': None, 'tipo': None, 'busqueda': ''}
        # Estrategia de ordenamiento para historial
        self.estrategia_orden = OrdenDescendente()
        # Estrategia de exportación
        self.export_strategy = ExportadorCSV()
        # Subject para Observer
        self.subject = Subject()
        self.subject.attach(self)
        self._build_ui()

    def update(self, event):
        if event == 'refrescar':
            self._load_current()

    def _build_ui(self):
        self.pack(fill='both', expand=True)
        self.tabs = ctk.CTkTabview(self)
        self.tabs.add('Pendientes')
        self.tabs.add('Historial')
        self.tabs.pack(fill='both', expand=True, padx=10, pady=10)

        self._build_pending_tab()
        self._build_history_tab()

    def _build_pending_tab(self):
        frame = self.tabs.tab('Pendientes')
        # Filtros en pendientes
        filt_frame = ctk.CTkFrame(frame)
        filt_frame.pack(fill='x', pady=5)
        ctk.CTkLabel(filt_frame, text="Sección:").pack(side='left', padx=(0,5))
        self.entry_seccion = ctk.CTkEntry(filt_frame, placeholder_text="Sección")
        self.entry_seccion.pack(side='left', padx=5)
        ctk.CTkLabel(filt_frame, text="Tipo:").pack(side='left', padx=(10,5))
        self.entry_tipo = ctk.CTkEntry(filt_frame, placeholder_text="Tipo")
        self.entry_tipo.pack(side='left', padx=5)
        ctk.CTkButton(filt_frame, text="Filtrar", command=self._apply_pending_filters).pack(side='left', padx=10)
        ctk.CTkButton(filt_frame, text="Limpiar", command=self._clear_pending_filters).pack(side='left')

        # Lista scrollable de pendientes
        self.scroll_pending = ctk.CTkScrollableFrame(frame)
        self.scroll_pending.pack(fill='both', expand=True, pady=5)

        # Botones exportación
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(fill='x', pady=5)
        ctk.CTkButton(btn_frame, text="Exportar CSV", command=lambda: self._export('csv')).pack(side='left', padx=5)
        ctk.CTkButton(btn_frame, text="Exportar PDF", command=lambda: self._export('pdf')).pack(side='left')

        # Carga inicial
        self._load_pending()

    def _build_history_tab(self):
        frame = self.tabs.tab('Historial')
        # Filtros en historial
        filt_frame = ctk.CTkFrame(frame)
        filt_frame.pack(fill='x', pady=5)
        ctk.CTkLabel(filt_frame, text="Desde (YYYY-MM-DD):").pack(side='left', padx=(0,5))
        self.entry_date_from = ctk.CTkEntry(filt_frame, placeholder_text="AAAA-MM-DD", width=100)
        self.entry_date_from.pack(side='left', padx=5)
        ctk.CTkLabel(filt_frame, text="Hasta:").pack(side='left', padx=(10,5))
        self.entry_date_to = ctk.CTkEntry(filt_frame, placeholder_text="AAAA-MM-DD", width=100)
        self.entry_date_to.pack(side='left', padx=5)
        ctk.CTkButton(filt_frame, text="Filtrar", command=self._apply_history_filters).pack(side='left', padx=10)
        ctk.CTkButton(filt_frame, text="Limpiar", command=self._clear_history_filters).pack(side='left')

        # Ordenamiento
        orden_frame = ctk.CTkFrame(frame)
        orden_frame.pack(fill='x', pady=5)
        self.option_order = ctk.CTkOptionMenu(orden_frame, values=["Descendente","Ascendente"], command=self._set_order)
        self.option_order.set("Descendente")
        self.option_order.pack(side='left', padx=5)

        # Tabla de historial
        cols = ("ID","Fecha","Sección","Tipo","Comentario","EstadoFinal","TurnoAsignado")
        self.tree_hist = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            self.tree_hist.heading(c, text=c)
        self.tree_hist.pack(fill='both', expand=True, pady=5)

        # Export botones
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(fill='x', pady=5)
        ctk.CTkButton(btn_frame, text="Exportar CSV", command=lambda: self._export('csv')).pack(side='left', padx=5)
        ctk.CTkButton(btn_frame, text="Exportar PDF", command=lambda: self._export('pdf')).pack(side='left')

        # Carga inicial
        self._load_history()

    def _apply_pending_filters(self):
        self.filtros['seccion'] = self.entry_seccion.get().strip() or None
        self.filtros['tipo'] = self.entry_tipo.get().strip() or None
        self._load_pending()

    def _clear_pending_filters(self):
        self.entry_seccion.delete(0,'end')
        self.entry_tipo.delete(0,'end')
        self.filtros['seccion'] = None
        self.filtros['tipo'] = None
        self._load_pending()

    def _apply_history_filters(self):
        df = self.entry_date_from.get().strip()
        dt = self.entry_date_to.get().strip()
        self.filtros['fecha_desde'] = datetime.fromisoformat(df) if df else None
        self.filtros['fecha_hasta'] = datetime.fromisoformat(dt) if dt else None
        self._load_history()

    def _clear_history_filters(self):
        self.entry_date_from.delete(0,'end')
        self.entry_date_to.delete(0,'end')
        self.filtros['fecha_desde'] = None
        self.filtros['fecha_hasta'] = None
        self._load_history()

    def _load_pending(self):
        for w in self.scroll_pending.winfo_children():
            w.destroy()
        regs = self.repo.get_pending(self.filtros)
        if not regs:
            ctk.CTkLabel(self.scroll_pending, text="No hay solicitudes pendientes.", font=(None,14)).pack(pady=20)
            return
        for sol in regs:
            f = ctk.CTkFrame(self.scroll_pending, corner_radius=6, fg_color="#f0f0f0")
            f.pack(fill='x', pady=5, padx=5)
            ctk.CTkLabel(f, text=f"#{sol.id} | {sol.nombre} | {sol.tipo} | {sol.seccion}").pack(side='left', padx=5)
            txt = ctk.CTkTextbox(f, height=3)
            txt.pack(side='left', padx=5, expand=True)
            ctk.CTkButton(f, text="Aceptar", command=lambda s=sol, t=txt: self._process(s, t, True)).pack(side='left', padx=2)
            ctk.CTkButton(f, text="Rechazar", command=lambda s=sol, t=txt: self._process(s, t, False)).pack(side='left')

    def _load_history(self):
        for r in self.tree_hist.get_children(): self.tree_hist.delete(r)
        regs = self.repo.get_history(self.filtros)
        regs = self.estrategia_orden.ordenar(regs)
        if not regs:
            self.tree_hist.insert('', 'end', values=("-","-","-","-","No hay registros","-","-"))
            return
        for rec in regs:
            vals = [rec.id, rec.fecha.strftime("%Y-%m-%d"), rec.seccion, rec.tipo,
                    rec.comentario, rec.estado_final, rec.turno_asignado]
            self.tree_hist.insert('', 'end', values=vals)

    def _set_order(self, val):
        self.estrategia_orden = OrdenAscendente() if 'Ascendente' in val else OrdenDescendente()
        self._load_history()

    def _process(self, sol, textbox, accept: bool):
        comment = textbox.get("1.0","end").strip()
        estado = 'aceptado' if accept else 'rechazado'
        turno = self.repo.rule_engine.assign(sol)
        ok = self.repo.resolve(sol.id, comment, estado, turno)
        if ok:
            messagebox.showinfo("Éxito", f"Solicitud {estado}. Turno: {turno}")
            self.subject.notify('refrescar')
        else:
            messagebox.showwarning("Error", "No se pudo procesar la solicitud.")

    def _export(self, fmt: str):
        data = self.repo.get_history(self.filtros) if self.vista_actual=='Historial' else self.repo.get_pending(self.filtros)
        if fmt=='csv':
            self.export_strategy = ExportadorCSV()
        else:
            self.export_strategy = ExportadorPDF()
        path = f"export_{self.vista_actual.lower()}.{fmt}"
        self.export_strategy.exportar(data, path)
        messagebox.showinfo("Exportación", f"Archivo guardado: {path}")

# Al final de views.py
if __name__ == '__main__':
    from mock_repo import MockRepo  # usar solo en pruebas
    app = ctk.CTk()
    vista = VistaRecepcionista(app, MockRepo())
    app.mainloop()