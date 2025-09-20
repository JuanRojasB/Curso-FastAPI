<<<<<<< HEAD
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
from typing import Optional
from datetime import date
=======
# schemas.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from enum import Enum
from typing import Optional
from datetime import date
import re
>>>>>>> 1cc8c586caa04b4276f7cc53c4733f5d17edbc69

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

<<<<<<< HEAD
class PsychologicalConsultationBase(BaseModel):
    reason_for_consultation: str
    preliminary_diagnosis: Optional[str] = None
    current_medication: Optional[str] = None
    first_session_date: date
    number_of_sessions: int = Field(ge=0)
    assigned_therapist: str
    observations: Optional[str] = None

=======
# Reglas principales:
# - reason_for_consultation: min_length=4
# - number_of_sessions: >=1 y <=60
# - assigned_therapist: debe incluir Dr./Dra. (o Dr / Dra sin punto)

class PsychologicalConsultationBase(BaseModel):
    reason_for_consultation: str = Field(..., min_length=4)
    preliminary_diagnosis: Optional[str] = None
    current_medication: Optional[str] = None
    first_session_date: date
    number_of_sessions: int = Field(..., ge=1, le=60)
    assigned_therapist: str
    observations: Optional[str] = None

    # Validar assigned_therapist (título)
    @field_validator("assigned_therapist")
    def validate_assigned_therapist(cls, v: str) -> str:
        # Acepta "Dr." / "Dra." o "Dr " / "Dra "
        if v.startswith("Dr.") or v.startswith("Dra.") or v.startswith("Dr ") or v.startswith("Dra "):
            return v
        # También acepta formatos tipo "Dr. Nombre Apellido" con regex más flexible
        if re.match(r"^(Dr|Dra)[\.\s].+$", v):
            return v
        raise ValueError("assigned_therapist must include 'Dr.' or 'Dra.' (o 'Dr ' / 'Dra ')")

>>>>>>> 1cc8c586caa04b4276f7cc53c4733f5d17edbc69
class PsychologicalConsultationCreate(PsychologicalConsultationBase):
    patient_id: int

class PsychologicalConsultationResponse(PsychologicalConsultationBase):
    id: int
    patient_id: int

    model_config = ConfigDict(from_attributes=True)

<<<<<<< HEAD
class PsychologicalConsultationUpdate(PsychologicalConsultationBase):
    # Optional fields can be updated
    reason_for_consultation: Optional[str] = None
    preliminary_diagnosis: Optional[str] = None
    current_medication: Optional[str] = None
    first_session_date: Optional[date] = None
    number_of_sessions: Optional[int] = Field(ge=0, default=None)
    assigned_therapist: Optional[str] = None
    observations: Optional[str] = None

# --- PSYCHOLOGICAL CONSULTATION ---

class PsychologicalConsultationPartialUpdate(PsychologicalConsultationBase):
    # All fields are optional for partial update
    reason_for_consultation: Optional[str] = None
    preliminary_diagnosis: Optional[str] = None
    current_medication: Optional[str] = None
    first_session_date: Optional[date] = None
    number_of_sessions: Optional[int] = Field(ge=0, default=None)
    assigned_therapist: Optional[str] = None
    observations: Optional[str] = None
=======
class PsychologicalConsultationUpdate(BaseModel):
    # Campos opcionales para update completo (puedes exigir algunos si lo prefieres)
    reason_for_consultation: Optional[str] = Field(None, min_length=4)
    preliminary_diagnosis: Optional[str] = None
    current_medication: Optional[str] = None
    first_session_date: Optional[date] = None
    number_of_sessions: Optional[int] = Field(None, ge=1, le=60)
    assigned_therapist: Optional[str] = None
    observations: Optional[str] = None

    @field_validator("assigned_therapist")
    def validate_assigned_therapist(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v.startswith("Dr.") or v.startswith("Dra.") or v.startswith("Dr ") or v.startswith("Dra "):
            return v
        if re.match(r"^(Dr|Dra)[\.\s].+$", v):
            return v
        raise ValueError("assigned_therapist must include 'Dr.' or 'Dra.' (o 'Dr ' / 'Dra ')")

class PsychologicalConsultationPartialUpdate(BaseModel):
    # Todos opcionales para patch
    reason_for_consultation: Optional[str] = Field(None, min_length=4)
    preliminary_diagnosis: Optional[str] = None
    current_medication: Optional[str] = None
    first_session_date: Optional[date] = None
    number_of_sessions: Optional[int] = Field(None, ge=1, le=60)
    assigned_therapist: Optional[str] = None
    observations: Optional[str] = None

    @field_validator("assigned_therapist")
    def validate_assigned_therapist(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v.startswith("Dr.") or v.startswith("Dra.") or v.startswith("Dr ") or v.startswith("Dra "):
            return v
        if re.match(r"^(Dr|Dra)[\.\s].+$", v):
            return v
        raise ValueError("assigned_therapist must include 'Dr.' or 'Dra.' (o 'Dr ' / 'Dra ')")
>>>>>>> 1cc8c586caa04b4276f7cc53c4733f5d17edbc69
