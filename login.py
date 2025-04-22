

import customtkinter as ctk
#import mysql.connector
from tkinter import messagebox

# Configuración de ventana
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Inicio de Sesión")
        self.geometry("400x400")

        self.label_titulo = ctk.CTkLabel(self, text="Iniciar Sesión", font=("Arial", 20))
        self.label_titulo.pack(pady=20)

        self.rut_entry = ctk.CTkEntry(self, placeholder_text="RUT")
        self.rut_entry.pack(pady=10)

        self.contrasena_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.contrasena_entry.pack(pady=10)

        self.boton_login = ctk.CTkButton(self, text="Ingresar", command=self.iniciar_sesion)
        self.boton_login.pack(pady=20)

    def iniciar_sesion(self):
        rut = self.rut_entry.get()
        contrasena = self.contrasena_entry.get()

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="tu_usuario",
                password="tu_contraseña",
                database="hospitrack"
            )
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT Nombre, TipoUsuario FROM dsoftware_usuario 
                WHERE RUT = %s AND Contrasenia = %s
            """, (rut, contrasena))
            resultado = cursor.fetchone()

            cursor.close()
            conexion.close()

            if resultado:
                nombre, tipo = resultado
                messagebox.showinfo("Bienvenido", f"Hola {nombre}, ingresaste como {tipo}")
                # Aquí puedes redirigir a otra ventana según el tipo de usuario
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {err}")

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
