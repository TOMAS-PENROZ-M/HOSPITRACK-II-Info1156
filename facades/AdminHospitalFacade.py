from models import CentroSaludDB
from database import get_db

class AdminHospitalFacade:
    """
    Esta clase implementa el patrón Facade.
    Su propósito es simplificar y centralizar las operaciones relacionadas con hospitales
    para que la interfaz gráfica no se acople directamente a la lógica de base de datos.
    """
    def __init__(self):
        self.db = next(get_db())

    def obtener_hospitales(self):
        """
        Retorna una lista con todos los hospitales registrados.
        """
        return self.db.query(CentroSaludDB).all()

    def agregar(self, nombre, lat, lon):
        """
        Agrega un nuevo hospital a la base de datos.
        """
        nuevo = CentroSaludDB(Nombre=nombre, Latitud=lat, Longitud=lon)
        self.db.add(nuevo)
        self.db.commit()

    def eliminar(self, hospital_id):
        """
        Elimina un hospital por su ID.
        """
        hospital = self.db.query(CentroSaludDB).filter_by(IdCentro=hospital_id).first()
        if hospital:
            self.db.delete(hospital)
            self.db.commit()
            return True
        return False

    def actualizar(self, hospital_id, nombre, lat, lon):
        """
        Actualiza los datos de un hospital por su ID.
        """
        hospital = self.db.query(CentroSaludDB).filter_by(IdCentro=hospital_id).first()
        if hospital:
            hospital.Nombre = nombre
            hospital.Latitud = lat
            hospital.Longitud = lon
            self.db.commit()
            return True
        return False
