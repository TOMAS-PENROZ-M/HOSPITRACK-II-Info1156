import bcrypt

def hashear_contrasena(password: str) -> str:
    """Hash + salt de la contraseña."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verificar_contrasena(password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra el hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))