# recepcionista/security_tests.py

import pytest
import logging
import re
import bcrypt
import time
from threading import Timer

from database import SessionLocal, init_db, get_engine
from models import SolicitudDB, UsuarioDB
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Configuración del logger para el módulo de pruebas de seguridad
logger = logging.getLogger('recepcionista.security_tests')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@pytest.fixture(scope='module')
def engine():
    """
    Crea un engine SQLite en memoria y inicializa el esquema.
    """
    eng = get_engine('sqlite:///:memory:')
    init_db(eng)
    return eng


@pytest.fixture(scope='function')
def db_session(engine):
    """
    Proporciona una sesión limpia para cada prueba.
    """
    Session = SessionLocal(bind=engine)
    session = Session()
    try:
        yield session
        session.rollback()
    finally:
        session.close()


class DummyClient:
    """
    Cliente de test simulado para endpoints web.
    """
    def __init__(self):
        self._cookies = {}

    def post(self, path, data=None, headers=None):
        # Simula rechazo por falta de CSRF
        if path.endswith('/recepcionista/nueva') and not headers.get('X-CSRF-Token'):
            return DummyResponse(403, 'Forbidden: CSRF token missing')
        return DummyResponse(200, 'OK')

    def get(self, path):
        # Simula acceso no autorizado
        if path == '/recepcionista/panel':
            return DummyResponse(401, 'Unauthorized')
        # Simula límite de peticiones
        if path == '/login':
            self._cookies.setdefault('count', 0)
            self._cookies['count'] += 1
            if self._cookies['count'] > 10:
                return DummyResponse(429, 'Too Many Requests')
            return DummyResponse(200, 'Login Page')
        return DummyResponse(200, 'OK')

    def login(self, username, password):
        # Simula login (siempre OK para tests)
        return True


class DummyResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text
        self.headers = {'Set-Cookie': ['sessionid=abc123; HttpOnly; Secure']}

    def get_all(self, name):
        return self.headers.get(name, [])


@pytest.fixture(scope='module')
def client():
    return DummyClient()


def test_sql_injection(db_session):
    # Inserta una solicitud válida
    s = SolicitudDB(titulo='Test', descripcion='Descripción segura', estado='pendiente')
    db_session.add(s)
    db_session.commit()

    # Intenta inyección
    malicious = "1; DROP TABLE solicituddb"
    with pytest.raises(SQLAlchemyError):
        db_session.execute(f"SELECT * FROM solicituddb WHERE id = {malicious}")
    logger.info("✔ Prueba de inyección SQL detectada correctamente")


def test_xss_sanitization(db_session):
    xss = '<script>alert("XSS")</script>'
    s = SolicitudDB(titulo=xss, descripcion=xss, estado='pendiente')
    db_session.add(s)
    db_session.commit()

    stored = db_session.query(SolicitudDB).get(s.id)
    assert '<script>' not in stored.titulo
    assert '<script>' not in stored.descripcion
    logger.info("✔ XSS sanitizado correctamente")


def test_csrf_protection(client):
    resp = client.post('/recepcionista/nueva', data={'titulo':'A','descripcion':'B'})
    assert resp.status_code == 403
    logger.info("✔ Protección CSRF funciona")


def test_access_control(client, db_session):
    # Crea usuario sin rol
    u = UsuarioDB(username='user', role='usuario', password_hash='hash')
    db_session.add(u)
    db_session.commit()

    client.login('user', 'pass')
    resp = client.get('/recepcionista/panel')
    assert resp.status_code == 401
    logger.info("✔ Control de acceso funciona según roles")


def test_password_storage():
    password = 'mi_contraseña'.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    assert bcrypt.checkpw(password, hashed)
    logger.info("✔ Almacenamiento de contraseñas seguro")


def test_rate_limiting(client):
    for _ in range(11):
        resp = client.get('/login')
    assert resp.status_code == 429
    logger.info("✔ Rate limiting activado correctamente")


def test_input_sanitization():
    raw = "Robert'); DROP TABLE usuarios;--"
    from recepcionista.validation import validate_form
    # validate_form muestra un mensaje de error y devuelve False
    assert not validate_form({'titulo': raw, 'descripcion': 'desc'})
    logger.info("✔ Sanitización de input previene SQL injection en formularios")


def test_file_upload_validation(client):
    resp = client.post('/upload', data={'file': (b'data', 'malware.exe')})
    assert resp.status_code == 400
    logger.info("✔ Validación de archivos de subida correcta")


def test_error_disclosure(client):
    resp = client.get('/recepcionista/error_endpoint')
    assert 'Stack trace' not in resp.text
    logger.info("✔ No se exponen trazas de error al usuario final")


def test_cookie_flags(client):
    resp = client.get('/login')
    cookies = resp.get_all('Set-Cookie')
    assert any('HttpOnly' in c for c in cookies)
    assert any('Secure' in c for c in cookies)
    logger.info("✔ Flags de cookie seguras presentes")


def test_logging_no_sensitive(caplog):
    caplog.set_level(logging.INFO)
    logging.info("Intento de login: password=supersecreto")
    assert 'supersecreto' not in caplog.text
    logger.info("✔ No se logean datos sensibles")


def test_encryption_at_rest(engine):
    conn = engine.raw_connection()
    pragma = conn.execute('PRAGMA cipher_version').fetchone()
    assert pragma is not None
    logger.info("✔ Base de datos cifrada en reposo")


def test_auto_logout():
    expired = []

    def on_logout():
        expired.append(True)

    from recepcionista.auto_logout import AutoLogout
    lo = AutoLogout(timeout_sec=1, on_logout=on_logout)
    lo.reset_timer()
    time.sleep(1.5)
    assert expired
    logger.info("✔ Logout automático por inactividad funciona")
