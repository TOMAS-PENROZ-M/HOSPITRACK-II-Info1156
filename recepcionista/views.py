import os
import sys
# Agrega la carpeta raíz del proyecto al path para importar módulos raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from database import SessionLocal
from models import SolicitudDB, UsuarioDB
from recepcionista.auto_logout import AutoLogout
from recepcionista.validation import FormValidator
from recepcionista.management import SolicitudManagerTest
from recepcionista.categorization import Categorizer

class RecepcionistaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Recepcionista - Hospitrack")
        self.geometry("900x600")
        self.session = SessionLocal()
        self.user = None
        self.auto_logout = None
        self.validator = FormValidator()
        self.categorizer = Categorizer()
        self._build_login()

    def _build_login(self):
        self._clear_window()
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.lbl_user = ctk.CTkLabel(self.login_frame, text="Usuario:")
        self.lbl_user.pack(pady=(50, 5))
        self.entry_user = ctk.CTkEntry(self.login_frame)
        self.entry_user.pack(pady=5)
        self.lbl_pass = ctk.CTkLabel(self.login_frame, text="Contraseña:")
        self.lbl_pass.pack(pady=5)
        self.entry_pass = ctk.CTkEntry(self.login_frame, show="*")
        self.entry_pass.pack(pady=5)
        self.btn_login = ctk.CTkButton(
            self.login_frame, text="Iniciar Sesión", command=self._login_action
        )
        self.btn_login.pack(pady=(20, 10))

    def _login_action(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        user = (
            self.session.query(UsuarioDB)
            .filter(UsuarioDB.username == username)
            .first()
        )
        if not user or not user.verify_password(password):
            messagebox.showerror("Error", "Credenciales inválidas")
            return
        self.user = user
        self._build_main()

    def _build_main(self):
        self._clear_window()
        self.auto_logout = AutoLogout(timeout_sec=300, on_logout=self._on_logout)
        self.bind_all("<Any-KeyPress>", lambda e: self.auto_logout.reset_timer())
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.lbl_title = ctk.CTkLabel(self.main_frame, text="Panel Recepcionista", font=("Arial", 24))
        self.lbl_title.pack(pady=10)
        self.btn_logout = ctk.CTkButton(self.main_frame, text="Cerrar Sesión", command=self._on_logout)
        self.btn_logout.pack(pady=5)
        self._build_request_section()
        self._build_form_section()

    def _build_request_section(self):
        self.request_frame = ctk.CTkFrame(self.main_frame)
        self.request_frame.pack(side="left", expand=True, fill="both", padx=(0,10))
        self.lbl_requests = ctk.CTkLabel(self.request_frame, text="Solicitudes Recibidas", font=("Arial", 18))
        self.lbl_requests.pack(pady=5)
        self.btn_refresh = ctk.CTkButton(self.request_frame, text="Refrescar", command=self._refresh_requests)
        self.btn_refresh.pack(pady=5)
        self.requests_list = ctk.CTkScrollableFrame(self.request_frame, width=400, height=400)
        self.requests_list.pack(pady=5, padx=5)
        self._refresh_requests()

    def _build_form_section(self):
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.pack(side="right", expand=True, fill="both", padx=(10,0))
        self.lbl_new = ctk.CTkLabel(self.form_frame, text="Nueva Solicitud (Prueba)", font=("Arial", 18))
        self.lbl_new.pack(pady=5)
        self.entry_title = ctk.CTkEntry(self.form_frame, placeholder_text="Título")
        self.entry_title.pack(pady=5)
        self.txt_description = ctk.CTkTextbox(self.form_frame, height=10)
        self.txt_description.pack(pady=5)
        self.lbl_priority = ctk.CTkLabel(self.form_frame, text="Prioridad Test")
        self.lbl_priority.pack(pady=5)
        self.btn_add = ctk.CTkButton(self.form_frame, text="Agregar", command=self._add_request)
        self.btn_add.pack(pady=5)
        self.btn_assign = ctk.CTkButton(self.form_frame, text="Asignar Pendientes", command=self._assign_test)
        self.btn_assign.pack(pady=5)

    def _refresh_requests(self):
        for widget in self.requests_list.winfo_children():
            widget.destroy()
        solicitudes = self.session.query(SolicitudDB).order_by(SolicitudDB.id).all()
        for sol in solicitudes:
            priority = self.categorizer.categorize(sol).value
            line = f"#{sol.id} {sol.titulo} - {sol.estado} ({priority})"
            lbl = ctk.CTkLabel(self.requests_list, text=line, anchor="w")
            lbl.pack(fill="x", pady=2, padx=5)

    def _add_request(self):
        titulo = self.entry_title.get().strip()
        descripcion = self.txt_description.get("1.0", "end").strip()
        if not self.validator.validate_and_show({"titulo": titulo, "descripcion": descripcion}):
            return
        nueva = SolicitudDB(titulo=titulo, descripcion=descripcion, estado="pendiente")
        self.session.add(nueva)
        self.session.commit()
        messagebox.showinfo("Éxito", "Solicitud agregada en modo prueba")
        self.entry_title.delete(0, "end")
        self.txt_description.delete("1.0", "end")
        self._refresh_requests()

    def _assign_test(self):
        manager = SolicitudManagerTest()
        manager.asignar_pruebas()
        self.session.commit()
        messagebox.showinfo("Asignar", "Solicitudes pendientes asignadas")
        self._refresh_requests()

    def _on_logout(self):
        if self.auto_logout:
            self.auto_logout.stop()
        self.user = None
        self._build_login()

    def _clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = RecepcionistaApp()
    app.mainloop()
