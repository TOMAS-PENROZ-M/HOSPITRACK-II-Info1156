from models import CentroSaludDB, UsuarioDB, ExpedienteMedicoDB
from database import get_db

class AdminHospitalFacade:
    """
    Facade para operaciones administrativas sobre hospitales, usuarios y expedientes médicos.
    """

    def __init__(self):
        self.db = next(get_db())

    # === HOSPITALES ===

    def obtener_hospitales(self):
        """Retorna una lista con todos los hospitales registrados."""
        return self.db.query(CentroSaludDB).all()

    def agregar_hospital(self, nombre, lat, lon):
        """Agrega un nuevo hospital."""
        nuevo = CentroSaludDB(Nombre=nombre, Latitud=lat, Longitud=lon)
        self.db.add(nuevo)
        self.db.commit()

    def eliminar_hospital(self, hospital_id):
        """Elimina un hospital por su ID."""
        hospital = self.db.query(CentroSaludDB).filter_by(IdCentro=hospital_id).first()
        if hospital:
            self.db.delete(hospital)
            self.db.commit()
            return True
        return False

    def actualizar_hospital(self, hospital_id, nombre, lat, lon):
        """Actualiza los datos de un hospital."""
        hospital = self.db.query(CentroSaludDB).filter_by(IdCentro=hospital_id).first()
        if hospital:
            hospital.Nombre = nombre
            hospital.Latitud = lat
            hospital.Longitud = lon
            self.db.commit()
            return True
        return False

    # === USUARIOS ===

    def obtener_usuarios(self):
        """Retorna una lista de todos los usuarios registrados."""
        return self.db.query(UsuarioDB).all()

    def agregar_usuario(self, rut, nombre, apellido, correo, telefono, tipo, contrasenia, fotourl=""):
        """Agrega un nuevo usuario."""
        nuevo = UsuarioDB(
            RUT=rut,
            Nombre=nombre,
            Apellido=apellido,
            CorreoElectronico=correo,
            NumeroTelefono=telefono,
            TipoUsuario=tipo,
            Contrasenia=contrasenia,
            fotourl=fotourl
        )
        self.db.add(nuevo)
        self.db.commit()

    def eliminar_usuario(self, rut):
        """Elimina un usuario por su RUT."""
        usuario = self.db.query(UsuarioDB).filter_by(RUT=rut).first()
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def actualizar_usuario(self, rut, **kwargs):
        """Actualiza los datos de un usuario por su RUT."""
        usuario = self.db.query(UsuarioDB).filter_by(RUT=rut).first()
        if usuario:
            for key, value in kwargs.items():
                setattr(usuario, key, value)
            self.db.commit()
            return True
        return False

    # === HISTORIAL / EXPEDIENTES MÉDICOS ===

    def obtener_expedientes_por_rut(self, rut):
        """Retorna la lista de expedientes médicos de un usuario dado su RUT."""
        usuario = self.db.query(UsuarioDB).filter_by(RUT=rut).first()
        return usuario.expedientes if usuario else []
