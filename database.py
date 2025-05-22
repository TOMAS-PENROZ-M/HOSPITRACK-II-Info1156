from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import CentroSaludDB, SeccionDB, EnEsperaDB
#from dotenv import load_dotenv
#import os
#from sshtunnel import SSHTunnelForwarder

# Por ahora solo se usará una base de datos local

engine = create_engine("sqlite:///hospitrack.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Crear todas las tablas en la base de datos
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    from datetime import datetime
    # Inicializar la base de datos
    init_db()
    print("Base de datos inicializada.")
    # Registros para testeo
    session = next(get_db())

    # Crear hospital
    nuevo_hospital = CentroSaludDB(Nombre="Hospital Test", Latitud=-33.4489, Longitud=-70.6693)
    session.add(nuevo_hospital)
    session.commit()
    print("Hospital creado.")
    # Agregarle una sección
    nueva_seccion = SeccionDB(NombreSeccion="Pediatría", IdCentro=nuevo_hospital.IdCentro)
    session.add(nueva_seccion)
    session.commit()
    print("Sección creada.")
    # Agregarle una fila de espera
    nueva_fila = EnEsperaDB(RUT="12345678-9", Prioridad=1, HoraRegistro=datetime.now(), IdSeccion=nueva_seccion.IdSeccion)
    session.add(nueva_fila)
    session.commit()
    print("Fila de espera creada.")

# Conexión a la base de datos en pillan, no funciona por ahora
'''
# Cargar las variables de entorno desde el archivo .env
load_dotenv()


usuario = os.getenv("DB_USER")
clave = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
puerto = os.getenv("DB_PORT")
base = os.getenv("DB_NAME")
ssh_usuario = os.getenv("SSH_USER")
ssh_clave = os.getenv("SSH_PASS")

# Configuración de la conexión SSH
tunnel = SSHTunnelForwarder(('pillan.inf.uct.cl', 22),
                            ssh_username=ssh_usuario,
                           ssh_password=ssh_clave,
                           remote_bind_address=('127.0.0.1', int(puerto)),
                           local_bind_address=('127.0.0.1', 3307))



# POR AHORA ESTO NO ESTÁ FUNCIONANDO !!!
try:
    # Iniciar el túnel SSH
    tunnel.start()

    # Crear la cadena de conexión a la base de datos
    connection_string = f"mysql+pymysql://{usuario}:{clave}@127.0.0.1:{tunnel.local_bind_port}/{base}"
    # Crear el motor de la base de datos
    engine = create_engine(connection_string, echo=True)
    # Crear la sesión
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Crear todas las tablas en la base de datos
    Base.metadata.create_all(bind=engine)

except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
finally:
    # Detener el túnel SSH
    tunnel.stop()
    print("Túnel SSH detenido.")
'''