from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, get_db
from typing import List

# Crear tablas (incluye las nuevas)
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="API Productos con Categorías")

# ENDPOINTS PARA Registrar e Identificar Usuario

@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si usuario ya existe
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Crear nuevo usuario
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    # Buscar usuario en BD
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verificar password
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Crear token
    access_token = create_access_token(username=user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }
    
    
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    """Obtener usuario actual desde token"""
    username = verify_token(token.credentials)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

# Endpoint público (sin protección)
@app.get("/products")
def get_products():
    return {"products": ["Laptop", "Phone", "Tablet"]}

# Endpoint protegido (necesita autenticación)
@app.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Endpoint solo para admin
@app.delete("/admin/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar si es admin (simplificado)
    if current_user.username != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Eliminar usuario
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()

    return {"message": "User deleted"}