import bcrypt

def _a_bytes(texto: str) -> bytes:
    return texto.encode('utf-8')

def generar_hash_contrasena(contrasena: str) -> str:
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(_a_bytes(contrasena), salt)
    return hash_bytes.decode('utf-8')

def verificar_contrasena(contrasena: str, hash_almacenado: str) -> bool:
    return bcrypt.checkpw(_a_bytes(contrasena), _a_bytes(hash_almacenado))
