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

    solicitudes = relationship('SolicitudDB', back_populates='usuario')
    respuestas = relationship('RespuestaSolicitudDB', back_populates='usuario_respondio')
    notificaciones = relationship('NotificacionDB', back_populates='usuario')
    expedientes = relationship('ExpedienteMedicoDB', back_populates='usuario')
    en_espera = relationship('EnEsperaDB', back_populates='usuario')

class CentroSaludDB(Base):
    __tablename__ = 'dsoftware_centrosalud'
    IdCentro = Column(Integer, primary_key=True)
    Latitud = Column(String(20))
    Longitud = Column(String(20))
    Nombre = Column(String(50))

    secciones = relationship('SeccionDB', back_populates='centro')

class SeccionDB(Base):
    __tablename__ = 'dsoftware_seccion'
    IdSeccion = Column(Integer, primary_key=True)
    IdCentro = Column(Integer, ForeignKey('dsoftware_centrosalud.IdCentro'))
    NombreSeccion = Column(String(30))
    Recepcionista = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))

    centro = relationship('CentroSaludDB', back_populates='secciones')
    solicitudes = relationship('SolicitudDB', back_populates='seccion')
    en_espera = relationship('EnEsperaDB', back_populates='seccion')

class SolicitudDB(Base):
    __tablename__ = 'dsoftware_solicitud'
    IdSolicitud = Column(Integer, primary_key=True)
    RUT = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))
    IdSeccion = Column(Integer, ForeignKey('dsoftware_seccion.IdSeccion'))
    Mensaje = Column(String(300))
    HoraSolicitud = Column(DateTime)
    Estado = Column(String(15))
    prioridad = Column(String(15))  # Ej: 'alta', 'media', 'baja'
    usuario = relationship('UsuarioDB', back_populates='solicitudes')
    seccion = relationship('SeccionDB', back_populates='solicitudes')
    respuestas = relationship('RespuestaSolicitudDB', back_populates='solicitud')
    Tipo = Column(String(20))  # Ej: 'consulta', 'examen', etc.

class RespuestaSolicitudDB(Base):
    __tablename__ = 'dsoftware_respuestasolicitud'
    Idrespuesta = Column(Integer, primary_key=True)
    IdSolicitud = Column(Integer, ForeignKey('dsoftware_solicitud.IdSolicitud'))
    UsuarioRespondio = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))
    Mensaje = Column(String(300))
    Estado = Column(String(15))

    solicitud = relationship('SolicitudDB', back_populates='respuestas')
    usuario_respondio = relationship('UsuarioDB', back_populates='respuestas')

class EnEsperaDB(Base):
    __tablename__ = 'dsoftware_enespera'
    IdRegistro = Column(Integer, primary_key=True)
    IdSeccion = Column(Integer, ForeignKey('dsoftware_seccion.IdSeccion'))
    RUT = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))
    HoraRegistro = Column(DateTime)
    Prioridad = Column(String(15))
    Tipo = Column(String(20))  # Ej: 'consulta', 'examen', etc.
    TurnoAsignado = Column(String(20), nullable=True)  # Ej: '10:00 AM', '12:30 PM', etc.

    seccion = relationship('SeccionDB', back_populates='en_espera')
    usuario = relationship('UsuarioDB', back_populates='en_espera')
    Comentario = Column(String(300), nullable=True)
    EstadoFinal = Column(String(20), nullable=True)  # Ej: 'aceptado', 'rechazado'
    FechaResolucion = Column(DateTime, nullable=True)

    seccion = relationship('SeccionDB', back_populates='en_espera')
    usuario = relationship('UsuarioDB', back_populates='en_espera')

class ExpedienteMedicoDB(Base):
    __tablename__ = 'dsoftware_expedientemedico'
    IdExpediente = Column(Integer, primary_key=True)
    RUT = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))
    ruta_archivo = Column(String(255))
    nombre_archivo = Column(String(255))

    usuario = relationship('UsuarioDB', back_populates='expedientes')

class NotificacionDB(Base):
    __tablename__ = 'dsoftware_notificacion'
    idnoti = Column(Integer, primary_key=True)
    UsuarioObjetivo = Column(String(9), ForeignKey('dsoftware_usuario.RUT'))
    mensaje = Column(String(300))
    leido = Column(Boolean)
    fecha = Column(DateTime)
    Idrespuesta = Column(Integer, ForeignKey('dsoftware_respuestasolicitud.Idrespuesta'))

    usuario = relationship('UsuarioDB', back_populates='notificaciones')
    respuesta = relationship('RespuestaSolicitudDB')
