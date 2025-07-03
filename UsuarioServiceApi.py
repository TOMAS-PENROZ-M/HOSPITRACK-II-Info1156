import requests

API_URL = "http://127.0.0.1:8000"

class UsuarioService:
    def obtener_usuario(self, rut):
        resp = requests.get(f"{API_URL}/usuarios/{rut}")
        if resp.status_code == 200:
            return resp.json()
        return None

    def actualizar_usuario(self, rut, correo, telefono):
        resp = requests.put(
            f"{API_URL}/usuarios/{rut}",
            data={"correo": correo, "telefono": telefono}
        )
        if resp.status_code == 200:
            return resp.json()["success"]
        return False
