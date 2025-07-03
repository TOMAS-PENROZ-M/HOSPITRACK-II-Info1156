import requests

API_URL = "http://127.0.0.1:8000"

class ExpedienteService:
    def listar_expedientes(self, rut):
        resp = requests.get(f"{API_URL}/expedientes/{rut}")
        if resp.status_code == 200:
            return resp.json()
        return []

    def eliminar_expediente(self, id_exp):
        resp = requests.delete(f"{API_URL}/expedientes/{id_exp}")
        if resp.status_code == 200:
            return resp.json()["success"]
        return False

    def subir_expediente(self, rut, file_path):
        file_name = file_path.split("/")[-1]
        with open(file_path, "rb") as f:
            files = {"file": (file_name, f)}
            resp = requests.post(
                f"{API_URL}/expedientes/{rut}",
                files=files
            )
        if resp.status_code == 200:
            return resp.json()["success"]
        return False
