import customtkinter as ctk
#import mysql.connector
from tkinter import messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class RegistroApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Registro de Usuario")
        self.geometry("400x600")

        self.rut = ctk.CTkEntry(self, placeholder_text="RUT")
        self.rut.pack(pady=10)

        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre")
        self.nombre.pack(pady=10)

        self.apellido = ctk.CTkEntry(self, placeholder_text="Apellido")
        self.apellido.pack(pady=10)

        self.correo = ctk.CTkEntry(self, placeholder_text="Correo Electrónico")
        self.correo.pack(pady=10)

        self.telefono = ctk.CTkEntry(self, placeholder_text="Número de Teléfono")
        self.telefono.pack(pady=10)

        self.tipo_usuario = ctk.CTkOptionMenu(self, values=["Admin", "UsuarioNormal", "Recepcionista"])
        self.tipo_usuario.pack(pady=10)
        self.tipo_usuario.set("UsuarioNormal")

        self.contrasena = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.contrasena.pack(pady=10)

        self.fotourl = ctk.CTkEntry(self, placeholder_text="URL de Foto")
        self.fotourl.pack(pady=10)

        self.btn_registrar = ctk.CTkButton(self, text="Registrarse", command=self.registrar_usuario)
        self.btn_registrar.pack(pady=20)

    def registrar_usuario(self):
        datos = (
            self.rut.get(),
            self.nombre.get(),
            self.apellido.get(),
            self.correo.get(),
            self.telefono.get(),
            self.tipo_usuario.get(),
            self.contrasena.get(),
            self.fotourl.get()
        )

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="tu_usuario",
                password="tu_contraseña",
                database="hospitrack"
            )
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO dsoftware_usuario 
                (RUT, Nombre, Apellido, CorreoElectronico, NumeroTelefono, TipoUsuario, Contrasenia, fotourl)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, datos)

            conexion.commit()
            cursor.close()
            conexion.close()

            messagebox.showinfo("Éxito", "Usuario registrado correctamente")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al registrar: {err}")

if __name__ == "__main__":
    app = RegistroApp()
    app.mainloop()
