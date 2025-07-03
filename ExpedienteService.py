import os
import shutil
from database import get_db
from models import UsuarioDB, ExpedienteMedicoDB

class ExpedienteService:
    upload_dir = "uploads"

    def subir_expediente(self, rut_usuario, expediente_path):
        name_file = os.path.basename(expediente_path)
        destino = os.path.join(self.upload_dir, name_file)

        os.makedirs(self.upload_dir, exist_ok=True)
        shutil.copy(expediente_path, destino)

        session = next(get_db())
        try:
            expediente = ExpedienteMedicoDB(
                RUT = rut_usuario,
                rut_usuario = destino,
                nombre_archivo = name_file
            )
            session.add(expediente)
            session.commit()
            return expediente
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def eliminar_expediente(self, id_exp):
        session = next(get_db())
        try:
            expediente = session.query(ExpedienteMedicoDB).filter_by(IdExpediente=id_exp).first()
            if expediente:
                if os.path.exists(expediente.ruta_archivo):
                    os.remove(expediente.ruta_archivo)
                session.delete(expediente)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def listar_expedientes(self, rut_usuario):
        session = next(get_db())
        try:
            expedientes = session.query(ExpedienteMedicoDB).filter_by(RUT=rut_usuario).all()
            return expedientes
        finally:
            session.close()