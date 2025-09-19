# auth.py

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .models import User

# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT (en producción usar variables de entorno)
SECRET_KEY = "mi-clave-super-secreta-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Convertir password a hash seguro"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar si password coincide con el hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(username: str) -> str:
    """Crear JWT token para un usuario"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": username,  # subject = usuario
        "exp": expire     # expiration = cuándo expira
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> str:
    """Verificar token y obtener username"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

# Funciones adicionales para la gestión de usuarios

def create_user(db: Session, username: str, email: str, password: str):
    """Crear usuario con password hasheado"""
    hashed_password = hash_password(password)

    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    """Obtener usuario por username"""
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    """Verificar usuario y password"""
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
