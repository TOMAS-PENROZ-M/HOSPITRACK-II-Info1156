import customtkinter as ctk
from tkinter import messagebox
from database import get_db
from models import CentroSaludDB
from PIL import Image
import os

class VistaAdmin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.db = next(get_db())
        self.selected_hospital_id = None

        # Ruta al logo
        logo_path = os.path.join(os.path.dirname(__file__), "..", "imagenes", "logo.png")
        logo_image = ctk.CTkImage(light_image=Image.open(logo_path), size=(200, 70))

        # Mostrar logo
        self.logo_label = ctk.CTkLabel(self, image=logo_image, text="")
        self.logo_label.grid(row=0, column=0, pady=(10, 5))

        # Título
        self.title_label = ctk.CTkLabel(self, text="Panel de Administrador", font=("Arial", 20, "bold"))
        self.title_label.grid(row=1, column=0, pady=10)

        # Lista de hospitales
        self.hospital_listbox = ctk.CTkTextbox(self, height=200, width=600)
        self.hospital_listbox.grid(row=2, column=0, padx=10, pady=10)
        self.hospital_listbox.bind("<ButtonRelease-1>", self.on_select_hospital)

        # Formulario
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=3, column=0, pady=10)

        self.nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Nombre del centro")
        self.nombre_entry.grid(row=0, column=0, padx=5, pady=5)

        self.lat_entry = ctk.CTkEntry(form_frame, placeholder_text="Latitud")
        self.lat_entry.grid(row=0, column=1, padx=5, pady=5)

        self.long_entry = ctk.CTkEntry(form_frame, placeholder_text="Longitud")
        self.long_entry.grid(row=0, column=2, padx=5, pady=5)

        # Botones
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=4, column=0, pady=10)

        self.add_btn = ctk.CTkButton(btn_frame, text="Agregar Hospital", command=self.agregar_hospital)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.update_btn = ctk.CTkButton(btn_frame, text="Actualizar Hospital", command=self.actualizar_hospital)
        self.update_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = ctk.CTkButton(btn_frame, text="Eliminar Hospital", command=self.eliminar_hospital)
        self.delete_btn.grid(row=0, column=2, padx=5)

        self.load_hospitales()

    def load_hospitales(self):
        self.hospital_listbox.delete("0.0", "end")
        hospitales = self.db.query(CentroSaludDB).all()
        for h in hospitales:
            self.hospital_listbox.insert("end", f"ID: {h.IdCentro} - {h.Nombre} ({h.Latitud}, {h.Longitud})\n")

    def agregar_hospital(self):
        nombre = self.nombre_entry.get()
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.long_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Latitud y longitud deben ser números.")
            return

        nuevo = CentroSaludDB(Nombre=nombre, Latitud=lat, Longitud=lon)
        self.db.add(nuevo)
        self.db.commit()
        messagebox.showinfo("Éxito", "Hospital agregado.")
        self.clear_form()
        self.load_hospitales()

    def eliminar_hospital(self):
        texto = self.hospital_listbox.get("insert linestart", "insert lineend")
        try:
            hospital_id = int(texto.split("ID: ")[1].split(" - ")[0])
            hospital = self.db.query(CentroSaludDB).filter_by(IdCentro=hospital_id).first()
            if hospital:
                self.db.delete(hospital)
                self.db.commit()
                messagebox.showinfo("Éxito", "Hospital eliminado.")
                self.clear_form()
                self.load_hospitales()
            else:
                messagebox.showerror("Error", "Hospital no encontrado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def on_select_hospital(self, event):
        try:
            index = self.hospital_listbox.index("@%s,%s" % (event.x, event.y))
            texto = self.hospital_listbox.get("%s linestart" % index, "%s lineend" % index)
            hospital_id = int(texto.split("ID: ")[1].split(" - ")[0])
            hospital = self.db.query(CentroSaludDB).filter_by(IdCentro=hospital_id).first()
            if hospital:
                self.selected_hospital_id = hospital.IdCentro
                self.nombre_entry.delete(0, "end")
                self.nombre_entry.insert(0, hospital.Nombre)
                self.lat_entry.delete(0, "end")
                self.lat_entry.insert(0, hospital.Latitud)
                self.long_entry.delete(0, "end")
                self.long_entry.insert(0, hospital.Longitud)
        except Exception as e:
            print("Error al seleccionar hospital:", e)

    def actualizar_hospital(self):
        if self.selected_hospital_id is None:
            messagebox.showwarning("Advertencia", "Selecciona un hospital para actualizar.")
            return

        try:
            hospital = self.db.query(CentroSaludDB).filter_by(IdCentro=self.selected_hospital_id).first()
            hospital.Nombre = self.nombre_entry.get()
            hospital.Latitud = self.lat_entry.get()
            hospital.Longitud = self.long_entry.get()
            self.db.commit()
            messagebox.showinfo("Éxito", "Hospital actualizado.")
            self.clear_form()
            self.load_hospitales()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def clear_form(self):
        self.selected_hospital_id = None
        self.nombre_entry.delete(0, "end")
        self.lat_entry.delete(0, "end")
        self.long_entry.delete(0, "end")
