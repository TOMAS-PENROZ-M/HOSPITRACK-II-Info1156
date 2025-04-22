from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class UsuarioDB(Base):
    __tablename__ = 'dsoftware_usuario'
    RUT = Column(String(9), primary_key=True)
    Nombre = Column(String(50))
    Apellido = Column(String(50))
    CorreoElectronico = Column(String(75))
    NumeroTelefono = Column(String(9))
    TipoUsuario = Column(String(20))
    Contrasenia = Column(String(255))
    fotourl = Column(String(255))

    solicitudes = relationship('Solicitud', back_populates='usuario')
    respuestas = relationship('RespuestaSolicitud', back_populates='usuario_respondio')
    notificaciones = relationship('Notificacion', back_populates='usuario')
    expedientes = relationship('ExpedienteMedico', back_populates='usuario')
    en_espera = relationship('EnEspera', back_populates='usuario')

class CentroSaludDB(Base):
    __tablename__ = 'dsoftware_centrosalud'
    IdCentro = Column(Integer, primary_key=True)
    Latitud = Column(String(20))
    Longitud = Column(String(20))
    Nombre = Column(String(50))

    secciones = relationship('Seccion', back_populates='centro')

class SeccionDB(Base):
    __tablename__ = 'dsoftware_seccion'
    IdSeccion = Column(Integer, primary_key=True)
    IdCentro = Column(Integer, ForeignKey('dsoftware_centrosalud.IdCentro'))
    NombreSeccion = Column(String(30))
    Recepcionista = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))

    centro = relationship('CentroSalud', back_populates='secciones')
    solicitudes = relationship('Solicitud', back_populates='seccion')
    en_espera = relationship('EnEspera', back_populates='seccion')

class SolicitudDB(Base):
    __tablename__ = 'dsoftware_solicitud'
    IdSolicitud = Column(Integer, primary_key=True)
    RUT = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))
    IdSeccion = Column(Integer, ForeignKey('dsoftware_seccion.IdSeccion'))
    Mensaje = Column(String(300))
    HoraSolicitud = Column(DateTime)
    Estado = Column(String(15))

    usuario = relationship('Usuario', back_populates='solicitudes')
    seccion = relationship('Seccion', back_populates='solicitudes')
    respuestas = relationship('RespuestaSolicitud', back_populates='solicitud')

class RespuestaSolicitudDB(Base):
    __tablename__ = 'dsoftware_respuestasolicitud'
    Idrespuesta = Column(Integer, primary_key=True)
    IdSolicitud = Column(Integer, ForeignKey('dsoftware_solicitud.IdSolicitud'))
    UsuarioRespondio = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))
    Mensaje = Column(String(300))
    Estado = Column(String(15))

    solicitud = relationship('Solicitud', back_populates='respuestas')
    usuario_respondio = relationship('Usuario', back_populates='respuestas')

class EnEsperaDB(Base):
    __tablename__ = 'dsoftware_enespera'
    IdRegistro = Column(Integer, primary_key=True)
    IdSeccion = Column(Integer, ForeignKey('dsoftware_seccion.IdSeccion'))
    RUT = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))
    HoraRegistro = Column(DateTime)
    Prioridad = Column(String(15))

    seccion = relationship('Seccion', back_populates='en_espera')
    usuario = relationship('Usuario', back_populates='en_espera')

class ExpedienteMedicoDB(Base):
    __tablename__ = 'dsoftware_expedientemedico'
    IdExpediente = Column(Integer, primary_key=True)
    RUT = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))
    ruta_archivo = Column(String(255))
    nombre_archivo = Column(String(255))

    usuario = relationship('Usuario', back_populates='expedientes')

class NotificacionDB(Base):
    __tablename__ = 'dsoftware_notificacion'
    idnoti = Column(Integer, primary_key=True)
    UsuarioObjetivo = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))
    mensaje = Column(String(300))
    leido = Column(Boolean)
    fecha = Column(DateTime)
    Idrespuesta = Column(Integer, ForeignKey('dsoftware_respuestasolicitud.Idrespuesta'))

    usuario = relationship('Usuario', back_populates='notificaciones')
    respuesta = relationship('RespuestaSolicitud')
