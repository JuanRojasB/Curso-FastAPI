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
    PsychologicalConsultationCreate, PsychologicalConsultationResponse,
    PsychologicalConsultationUpdate, PsychologicalConsultationPartialUpdate
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
    "/psych_consultas",
    response_model=PsychologicalConsultationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_consultation(consultation: PsychologicalConsultationCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_consultation = models.PsychologicalConsultation(**consultation.model_dump())
    db.add(db_consultation)
    db.commit()
    db.refresh(db_consultation)
    return db_consultation


@app.get("/psych_consultas", response_model=List[PsychologicalConsultationResponse])
def list_psych_consultas(skip: int = 0, limit: int = 10, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    psych_consultas = db.query(models.PsychologicalConsultation).offset(skip).limit(limit).all()
    return psych_consultas


@app.get("/psych_consultas/{entity_id}", response_model=PsychologicalConsultationResponse)
def get_consultation_by_id(
    entity_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_consultation = db.query(models.PsychologicalConsultation).filter(models.PsychologicalConsultation.id == entity_id).first()
    if not db_consultation:
        raise HTTPException(status_code=404, detail="Not Found")
    return db_consultation


@app.put("/psych_consultas/{entity_id}", response_model=PsychologicalConsultationResponse)
def update_consultation(
    entity_id: int,
    consultation: PsychologicalConsultationUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_consultation = db.query(models.PsychologicalConsultation).filter(models.PsychologicalConsultation.id == entity_id).first()
    if not db_consultation:
        raise HTTPException(status_code=404, detail="Not Found")

    for key, value in consultation.model_dump(exclude_unset=True).items():
        setattr(db_consultation, key, value)

    db.commit()
    db.refresh(db_consultation)
    return db_consultation


@app.patch("/psych_consultas/{entity_id}", response_model=PsychologicalConsultationResponse)
def partial_update_consultation(
    entity_id: int,
    consultation: PsychologicalConsultationPartialUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_consultation = db.query(models.PsychologicalConsultation).filter(models.PsychologicalConsultation.id == entity_id).first()
    if not db_consultation:
        raise HTTPException(status_code=404, detail="Not Found")

    for key, value in consultation.model_dump(exclude_unset=True).items():
        setattr(db_consultation, key, value)

    db.commit()
    db.refresh(db_consultation)
    return db_consultation


# --- DELETE ENDPOINTS ---

@app.delete("/psych_consultas/{entity_id}", status_code=status.HTTP_200_OK)
def delete_consultation(
    entity_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_consultation = db.query(models.PsychologicalConsultation).filter(models.PsychologicalConsultation.id == entity_id).first()
    if not db_consultation:
        raise HTTPException(status_code=404, detail="Not Found")
    
    db.delete(db_consultation)
    db.commit()
    return {"detail": "Consultation deleted successfully"}


@app.delete("/psych_consultas/{entity_id}", status_code=status.HTTP_404_NOT_FOUND)
def delete_consultation_not_found(
    entity_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_consultation = db.query(models.PsychologicalConsultation).filter(models.PsychologicalConsultation.id == entity_id).first()
    if not db_consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    db.delete(db_consultation)
    db.commit()
    return {"detail": "Consultation not found"}

