from sqlalchemy import Column, Integer, String, Boolean, Enum as SqlEnum, Date, ForeignKey
from sqlalchemy.orm import relationship
import enum
from database import Base  # Importa la base declarativa

class UserRoleEnum(str, enum.Enum):
    admin = "admin"
    psychologist = "psychologist"
    patient = "patient"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SqlEnum(UserRoleEnum), nullable=False, default=UserRoleEnum.patient)
    is_active = Column(Boolean, default=True)

# --- Modelo Patient ---

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    medical_history = Column(String, nullable=True)
    emergency_contact = Column(String, nullable=False)

    # Relación con consultas psicológicas
    consultations = relationship("PsychologicalConsultation", back_populates="patient")

# --- Modelo PsychologicalConsultation ---

class PsychologicalConsultation(Base):
    __tablename__ = "psychological_consultations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    reason_for_consultation = Column(String, nullable=False)
    preliminary_diagnosis = Column(String, nullable=True)
    assigned_therapist = Column(String, nullable=False)
    current_medication = Column(String, nullable=True)
    first_session_date = Column(Date, nullable=False)
    number_of_sessions = Column(Integer, nullable=False)
    observations = Column(String, nullable=True)

    # Relación con paciente
    patient = relationship("Patient", back_populates="consultations")
