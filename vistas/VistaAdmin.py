import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os

from facades.AdminHospitalFacade import AdminHospitalFacade
from commands.AgregarHospitalCommand import AgregarHospitalCommand


class VistaAdmin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.facade = AdminHospitalFacade()
        self.selected_hospital_id = None
        self.selected_user_rut = None

        # Mapas de tipos de usuario
        self.tipo_usuario_map = {
            "Administrador": "Administrador",
            "UsuarioNormal": "Usuario",
            "Recepcionista": "Recepcionista",
        }
        self.tipo_usuario_reverse_map = {v: k for k, v in self.tipo_usuario_map.items()}

        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), "..", "imagenes", "logo.png")
        logo_image = ctk.CTkImage(light_image=Image.open(logo_path), size=(200, 70))
        self.logo_label = ctk.CTkLabel(self, image=logo_image, text="")
        self.logo_label.grid(row=0, column=0, pady=(10, 5))

        # Título
        self.title_label = ctk.CTkLabel(self, text="Panel de Administrador", font=("Arial", 20, "bold"))
        self.title_label.grid(row=1, column=0, pady=10)

        # Lista de hospitales
        self.hospital_listbox = ctk.CTkTextbox(self, height=200, width=600)
        self.hospital_listbox.grid(row=2, column=0, padx=10, pady=10)
        self.hospital_listbox.bind("<ButtonRelease-1>", self.on_select_hospital)

        # Formulario hospital
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=3, column=0, pady=10)

        self.nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Nombre del centro")
        self.nombre_entry.grid(row=0, column=0, padx=5, pady=5)

        self.lat_entry = ctk.CTkEntry(form_frame, placeholder_text="Latitud")
        self.lat_entry.grid(row=0, column=1, padx=5, pady=5)

        self.long_entry = ctk.CTkEntry(form_frame, placeholder_text="Longitud")
        self.long_entry.grid(row=0, column=2, padx=5, pady=5)

        # Botones hospital
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=4, column=0, pady=10)
        ctk.CTkButton(btn_frame, text="Agregar Hospital", command=self.agregar_hospital).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Actualizar Hospital", command=self.actualizar_hospital).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar Hospital", command=self.eliminar_hospital).grid(row=0, column=2, padx=5)

        # Formulario usuario reducido
        user_form = ctk.CTkFrame(self)
        user_form.grid(row=5, column=0, pady=10)

        self.rut_entry = ctk.CTkEntry(user_form, placeholder_text="RUT")
        self.rut_entry.grid(row=0, column=0, padx=5, pady=5)

        self.tipo_var = ctk.StringVar()
        self.tipo_menu = ctk.CTkOptionMenu(user_form, variable=self.tipo_var, values=list(self.tipo_usuario_map.values()))
        self.tipo_menu.grid(row=0, column=1, padx=5, pady=5)

        # Dropdown usuario
        self.user_dropdown_var = ctk.StringVar()
        self.user_dropdown = ctk.CTkOptionMenu(user_form, variable=self.user_dropdown_var, values=[], command=self.on_user_dropdown_select)
        self.user_dropdown.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Botones usuario
        user_btn_frame = ctk.CTkFrame(self)
        user_btn_frame.grid(row=6, column=0, pady=10)
        ctk.CTkButton(user_btn_frame, text="Actualizar Usuario", command=self.actualizar_usuario).grid(row=0, column=0, padx=5)
        ctk.CTkButton(user_btn_frame, text="Eliminar Usuario", command=self.eliminar_usuario).grid(row=0, column=1, padx=5)

        self.load_hospitales()
        self.load_usuarios()

    def load_hospitales(self):
        self.hospital_listbox.delete("0.0", "end")
        for h in self.facade.obtener_hospitales():
            self.hospital_listbox.insert("end", f"ID: {h.IdCentro} - {h.Nombre} ({h.Latitud}, {h.Longitud})\n")

    def load_usuarios(self):
        usuarios = self.facade.obtener_usuarios()
        options = [
            f"{u.RUT} - {u.Nombre} {u.Apellido} ({self.tipo_usuario_map.get(u.TipoUsuario, u.TipoUsuario)})"
            for u in usuarios
        ]
        self.user_dropdown.configure(values=options)
        self.user_dropdown.set("Seleccionar usuario")

    def on_select_hospital(self, event):
        try:
            index = self.hospital_listbox.index("@%s,%s" % (event.x, event.y))
            texto = self.hospital_listbox.get("%s linestart" % index, "%s lineend" % index)
            hospital_id = int(texto.split("ID: ")[1].split(" - ")[0])
            hospital = next((h for h in self.facade.obtener_hospitales() if h.IdCentro == hospital_id), None)
            if hospital:
                self.selected_hospital_id = hospital.IdCentro
                self.nombre_entry.delete(0, "end")
                self.nombre_entry.insert(0, hospital.Nombre)
                self.lat_entry.delete(0, "end")
                self.lat_entry.insert(0, hospital.Latitud)
                self.long_entry.delete(0, "end")
                self.long_entry.insert(0, hospital.Longitud)
        except Exception:
            pass

    def agregar_hospital(self):
        nombre = self.nombre_entry.get()
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.long_entry.get())
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Latitud debe estar entre -90 y 90, longitud entre -180 y 180.")
            return
        AgregarHospitalCommand(self.facade, nombre, lat, lon).ejecutar()
        messagebox.showinfo("Éxito", "Hospital agregado.")
        self.clear_form()
        self.load_hospitales()

    def actualizar_hospital(self):
        if self.selected_hospital_id is None:
            messagebox.showwarning("Advertencia", "Selecciona un hospital.")
            return
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.long_entry.get())
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError
            if self.facade.actualizar_hospital(self.selected_hospital_id, self.nombre_entry.get(), lat, lon):
                messagebox.showinfo("Éxito", "Hospital actualizado.")
                self.clear_form()
                self.load_hospitales()
            else:
                messagebox.showerror("Error", "No se encontró el hospital.")
        except ValueError:
            messagebox.showerror("Error", "Latitud o longitud inválida.")

    def eliminar_hospital(self):
        texto = self.hospital_listbox.get("insert linestart", "insert lineend")
        try:
            hospital_id = int(texto.split("ID: ")[1].split(" - ")[0])
            if self.facade.eliminar_hospital(hospital_id):
                messagebox.showinfo("Éxito", "Hospital eliminado.")
                self.clear_form()
                self.load_hospitales()
            else:
                messagebox.showerror("Error", "No se encontró el hospital.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {e}")

    def on_user_dropdown_select(self, selection):
        try:
            rut = selection.split(" - ")[0].strip()
            usuario = next((u for u in self.facade.obtener_usuarios() if u.RUT == rut), None)
            if usuario:
                self.selected_user_rut = rut
                self.rut_entry.delete(0, "end")
                self.rut_entry.insert(0, usuario.RUT)
                tipo_legible = self.tipo_usuario_map.get(usuario.TipoUsuario, usuario.TipoUsuario)
                self.tipo_var.set(tipo_legible)
        except Exception as e:
            print("Error al seleccionar usuario:", e)

    def actualizar_usuario(self):
        if not self.selected_user_rut:
            messagebox.showwarning("Advertencia", "Selecciona un usuario.")
            return
        nuevo_tipo = self.tipo_usuario_reverse_map.get(self.tipo_var.get(), self.tipo_var.get())
        actualizado = self.facade.actualizar_usuario(
            self.selected_user_rut,
            TipoUsuario=nuevo_tipo
        )
        if actualizado:
            messagebox.showinfo("Éxito", "Tipo de usuario actualizado.")
            self.clear_form()
            self.load_usuarios()
        else:
            messagebox.showerror("Error", "No se encontró el usuario.")

    def eliminar_usuario(self):
        if not self.selected_user_rut:
            messagebox.showwarning("Advertencia", "Selecciona un usuario.")
            return
        if self.facade.eliminar_usuario(self.selected_user_rut):
            messagebox.showinfo("Éxito", "Usuario eliminado.")
            self.clear_form()
            self.load_usuarios()
        else:
            messagebox.showerror("Error", "No se encontró el usuario.")

    def clear_form(self):
        self.selected_hospital_id = None
        self.nombre_entry.delete(0, "end")
        self.lat_entry.delete(0, "end")
        self.long_entry.delete(0, "end")
        self.selected_user_rut = None
        self.rut_entry.delete(0, "end")
        self.tipo_var.set("")
