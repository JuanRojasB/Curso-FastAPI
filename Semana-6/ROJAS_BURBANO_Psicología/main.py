from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

import models
from database import SessionLocal, engine
from schemas import (
    UserCreate, UserResponse, Token, LoginRequest,
    PatientCreate, PatientResponse,
    PsychologicalConsultationCreate, PsychologicalConsultationResponse
)
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token,
)

app = FastAPI(title="Psychology Consultation API")
security = HTTPBearer()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- AUTH ---

@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email is already registered")

    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role=user.role,
        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login", response_model=Token)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }


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


@app.get("/profile", response_model=UserResponse)
def get_user_profile(current_user: models.User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active
    )


# --- PATIENTS ---

@app.post("/patients", response_model=PatientResponse)
def create_patient(patient: PatientCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@app.get("/patients", response_model=List[PatientResponse])
def list_patients(skip: int = 0, limit: int = 10, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients


# --- PSYCHOLOGICAL CONSULTATIONS ---

@app.post(
    "/consultations",
    response_model=PsychologicalConsultationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_consultation(consultation: PsychologicalConsultationCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_consultation = models.PsychologicalConsultation(**consultation.model_dump())
    db.add(db_consultation)
    db.commit()
    db.refresh(db_consultation)
    return db_consultation


@app.get("/consultations", response_model=List[PsychologicalConsultationResponse])
def list_consultations(skip: int = 0, limit: int = 10, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    consultations = db.query(models.PsychologicalConsultation).offset(skip).limit(limit).all()
    return consultations
