# auth.py
from passlib.context import CryptContext

# Configurar hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Convertir password a hash"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar si password coincide con hash"""
    return pwd_context.verify(plain_password, hashed_password)