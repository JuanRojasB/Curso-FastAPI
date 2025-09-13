from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
from typing import Optional
from datetime import date


# --- ENUMS ---

class UserRole(str, Enum):
    admin = "admin"
    psychologist = "psychologist"
    patient = "patient"


# --- AUTH & USERS ---

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class LoginRequest(BaseModel):
    username: str
    password: str


# --- PATIENTS ---

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    phone_number: str
    email: EmailStr
    medical_history: Optional[str] = None
    emergency_contact: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- PSYCHOLOGICAL CONSULTATION ---

class PsychologicalConsultationBase(BaseModel):
    reason_for_consultation: str
    preliminary_diagnosis: Optional[str] = None
    current_medication: Optional[str] = None
    first_session_date: date
    number_of_sessions: int = Field(ge=0)
    assigned_therapist: str
    observations: Optional[str] = None


class PsychologicalConsultationCreate(PsychologicalConsultationBase):
    patient_id: int


class PsychologicalConsultationResponse(PsychologicalConsultationBase):
    id: int
    patient_id: int

    model_config = ConfigDict(from_attributes=True)
