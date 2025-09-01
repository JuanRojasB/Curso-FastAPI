# jwt_handler.py
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "tu_clave_super_secreta"  # En producción: variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(username: str) -> str:
    """Crear token para un usuario"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": username,  # subject = usuario
        "exp": expire     # expiration = cuándo expira
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> str:
    """Verificar token y obtener username"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except jwt.PyJWTError:
        return None  # Token inválido