from tkinter import filedialog
from tkinter import messagebox
import shutil
import os
from database import get_db
from models import ExpedienteMedicoDB

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
        except Excepcion as e:
            session.rollback()
            messagebox.showerror("Error", f"No se pudo subir correctamente el archivo{e}")
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
            #Aqui añadir el metodo de cargar exp
        else:
            messagebox.showwarning("No encontrado", "No se encontro el expediente con ese id")
    except Excepcion as e:
        session.rollback()
        messagebox.showerror("Error", f"No se pudo eliminar correctamente el expediente{e}")
    finally:
        session.close()