from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base
import os
from sshtunnel import SSHTunnelForwarder


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
                           remote_bind_address=('127.0.0.1', 3306),
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