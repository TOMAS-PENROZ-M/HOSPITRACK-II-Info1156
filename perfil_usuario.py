import customtkinter as ctk
from tkinter import filedialog, messagebox
import shutil
import os
from database import get_db
from models import UsuarioDB, ExpedienteMedicoDB

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")  

class PerfilUsuarioApp(ctk.CTk):
    def __init__(self, rut_usuario):
        super().__init__()

        self.title("Perfil usuario")
        self.geometry("500x500")
        self.rut_usuario = rut_usuario

        self.label_titulo = ctk.CTkLabel(self, text = "Perfil usuario", font=("Arial", 24))
        self.label_titulo.pack(pady=20)

        self.info_usuario = ctk.CTkTextbox(self, width=450, height=100)
        self.info_usuario.pack(pady=10)
        self.info_usuario.configure(state="disabled")

        self.entry_telefono = ctk.CTkEntry(self, placeholder_text="Ingresa el nuevo numero de telefono")
        self.entry_telefono.pack(pady=5)

        self.entry_correo = ctk.CTkEntry(self, placeholder_text="Ingresa el nuevo correo electronico")
        self.entry_correo.pack(pady=5)

        self.btn_actualizar_datos = ctk.CTkButton(self, text="Actualizar datos", command=self.actualizar_datos_usuario)
        self.btn_actualizar_datos.pack(pady=10)

        self.btn_gestion_expedientes = ctk.CTkButton(self, text="Gestion de expedientes", command=self.abrir_gestion_expedientes)
        self.btn_gestion_expedientes.pack(pady=10)

        self.cargar_datos_usuario

    def cargar_datos_usuario(self):
        session = next(get_db())
        try:
            usuario = session.query(UsuarioDB).filter_by(RUT=self.rut_usuario).first()
            if usuario:
                texto = f"""
Nombre = {usuario.Nombre}
Apellido = {usuario.Apellido}
Correo = {usuario.CorreoElectronico}
Telefono = {usuario.NumeroTelefono}
"""
                self.info_usuario.configure(state="Normal")
                self.info_usuario.delete("1.0", "end")
                self.info_usuario.insert("end", texto.strip())
                self.info_usuario.configure(state="disabled")
            else:
                messagebox.showwarning("Usuario no encontrado","No se encontro la informacion del usuario")
        finally:
            session.close()

    def abrir_gestion_expedientes(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Mis expedientes")
        ventana.geometry("500x450")

        self.lista_exp = ctk.CTkTextbox(self, width=460, height=200)
        self.lista_exp.pack(pady=10)

        self.id_a_eliminar = ctk.CTkEntry(ventana, placeholder_text="id del expediente a eliminar")
        self.id_a_eliminar.pack(pady=5)

        btn_eliminar = ctk.CTkButton(ventana, text="Eliminar expediente", command=self.delete_exp)
        btn_eliminar.pack(pady=5)

        btn_agregar = ctk.CTkButton(ventana, text="Agregar expediente", command=self.subir_exp)
        btn_agregar.pack(pady=5)

        self.cargar_expedientes()

    def cargar_expedientes(self):
        self.lista_exp.delete("1.0", "end")
        session = next(get_db())
        try:
            expedientes = session.query(ExpedienteMedicoDB).filter_by(RUT=self.rut_usuario).all()
            if expedientes:
                for exp in expedientes:
                    self.lista_exp.insert("end", f"Id : {exp.IdExpediente} | Nombre : {exp.nombre_archivo}\n")
                else:
                    self.lista_exp.insert("end", "no hay expedientes registrados")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los expedientes : {e}")
        finally:
            session.close()

    def delete_exp(self):
        id_texto = self.id_a_eliminar.get()
        if not id_texto.isdigit():
            messagebox.showwarning("Entrada invalida", "Debes ingresar un id valido")
            return
        
        id_exp = int(id_texto)
        session = next(get_db())
        try:
            expediente = session.query(ExpedienteMedicoDB).filter_by(IdExpediente= id_exp).first
            if expediente:
                if os.path.exists(expediente.destino_exp):
                    os.remove(expediente.destino_exp)    
                session.delete(expediente)
                session.commit()
                messagebox.showinfo("Exito", "Expediente eliminado corrrectamente")
                self.cargar_expedientes()
            else:
                messagebox.showwarning("No encontrado", "No se encontro el expediente con ese id")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar correctamente el expediente{e}")
        finally:
            session.close()

    def subir_exp(self):
        expediente_path = filedialog.askopenfilename(
            filetypes=[("Todos los archivo", "*.*"),
                    ("PDF files", "*.pdf"),
                    ("WORD files", "*.docx"),
                    ("Imagenes", "*.jpg;*.jpeg;*.png")]
        )
        
        if expediente_path:
            name_file = os.path.basename(expediente_path)
            destino = os.path.join("uploads", name_file)

            os.makedirs("uploads", exist_ok=True)
            shutil.copy(expediente_path, destino)

            user_RUT = self.rut.get()
            session = next(get_db())
            try:
                expediente = ExpedienteMedicoDB(
                    RUT = user_RUT,
                    destino_exp = destino,
                    nombre_exp = name_file
                    )
                session.add(expediente)
                session.commit()
                messagebox.showinfo("Exito", "Expediente subido corrrectamente")
                self.cargar_expedientes()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Error", f"No se pudo subir correctamente el archivo{e}")
            finally:
                session.close()

    def actualizar_datos_usuario(self):
        nuevo_correo = self.entry_correo.get().strip()
        nuevo_telefono = self.entry_telefono.get().strip()

        if not nuevo_correo or not nuevo_telefono:
            messagebox.showwarning("Campos invalidos", "Por favor complete los campos")
            return
        
        if len(nuevo_telefono) != 9 or not nuevo_telefono.isdigit():
            messagebox.showwarning("Telefono invalido", "El telefono debe tener 9 numeros")
            return
        
        session = next(get_db())
        try:
            usuario = session.query(UsuarioDB).filter_by(RUT=self.rut_usuario).first()
            if usuario:
                usuario.CorreoElectronico = nuevo_correo
                usuario.NumeroTelefono = nuevo_telefono
                session.commit()
                messagebox.showinfo("Datos actualizados correctamente")
                self.cargar_datos_usuario()
                self.entry_correo.delete(0, "end")
                self.entry_telefono.delete(0, "end")
            else:
                messagebox.showerror("Error", "Usuario no encontrado")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"No se puedo actualizar: {e}")
        finally:
            session.close()

if __name__ == "__main__":
    app = PerfilUsuarioApp(rut_usuario=12344556)
    app.mainloop()