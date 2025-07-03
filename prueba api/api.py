from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel

app = FastAPI()

# Simulación de datos
fake_db_users = {
    12344556: {
        "Nombre": "Juan",
        "Apellido": "Perez",
        "CorreoElectronico": "juan@example.com",
        "NumeroTelefono": "987654321"
    }
}

fake_expedientes = [
    {"IdExpediente": 1, "nombre_archivo": "archivo1.pdf", "usuario_rut": 12344556},
    {"IdExpediente": 2, "nombre_archivo": "imagen.png", "usuario_rut": 12344556}
]

class Usuario(BaseModel):
    Nombre: str
    Apellido: str
    CorreoElectronico: str
    NumeroTelefono: str

@app.get("/usuarios/{rut}", response_model=Usuario)
def obtener_usuario(rut: int):
    usuario = fake_db_users.get(rut)
    if usuario:
        return usuario
    return None

@app.put("/usuarios/{rut}")
def actualizar_usuario(rut: int, correo: str = Form(...), telefono: str = Form(...)):
    if rut in fake_db_users:
        fake_db_users[rut]["CorreoElectronico"] = correo
        fake_db_users[rut]["NumeroTelefono"] = telefono
        return {"success": True}
    return {"success": False}

@app.get("/expedientes/{rut}")
def listar_expedientes(rut: int):
    return [e for e in fake_expedientes if e["usuario_rut"] == rut]

@app.delete("/expedientes/{id_exp}")
def eliminar_expediente(id_exp: int):
    global fake_expedientes
    before = len(fake_expedientes)
    fake_expedientes = [e for e in fake_expedientes if e["IdExpediente"] != id_exp]
    return {"success": len(fake_expedientes) < before}

@app.post("/expedientes/{rut}")
def subir_expediente(rut: int, file: UploadFile):
    fake_expedientes.append({
        "IdExpediente": len(fake_expedientes)+1,
        "nombre_archivo": file.filename,
        "usuario_rut": rut
    })
    return {"success": True}