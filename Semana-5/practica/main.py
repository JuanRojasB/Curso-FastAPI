# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from . import auth, models
from .database import SessionLocal, engine
from .schemas import UserCreate, UserResponse, Token, LoginRequest, UserRegister, UserLogin
from .auth import hash_password, verify_password, create_access_token, verify_token

# Crear la aplicación FastAPI
app = FastAPI(title="API con Autenticación Básica")
security = HTTPBearer()

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint público para comparar
@app.get("/")
def read_root():
    return {"message": "API pública sin autenticación"}

# Endpoint de registro de usuario
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si usuario ya existe
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Verificar si email ya existe
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Crear usuario con password hasheado
    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# Endpoint de login
@app.post("/login", response_model=Token)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario
    user = db.query(models.User).filter(models.User.username == login_data.username).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Verificar password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Crear token
    access_token = create_access_token(username=user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }

# Dependency para obtener usuario actual
def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = verify_token(token.credentials)
    if username is None:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception

    return user

# Endpoint protegido de ejemplo
@app.get("/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Endpoint de registro de usuario usando otro modelo (UserRegister)
@app.post("/register", response_model=UserResponse)
def register_user_v2(user_data: UserRegister, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""

    # Verificar si usuario ya existe
    if auth.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Username ya está registrado"
        )

    # Crear usuario
    user = auth.create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active
    )

# Endpoint de login y obtener token
@app.post("/login", response_model=Token)
def login_user_v2(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login y obtener token"""

    # Autenticar usuario
    user = auth.authenticate_user(db, user_data.username, user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o password incorrecto",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token
    access_token_expires = timedelta(minutes=30)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

# Endpoint protegido de usuario actual
@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(auth.get_current_user)):
    """Obtener usuario actual"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active
    )
