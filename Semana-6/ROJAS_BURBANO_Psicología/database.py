from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# URL de la base de datos (puede venir de variable de entorno)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./psych_.db")

# Crear engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos (aquí definimos Base)
Base = declarative_base()

# Función para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear tablas si no existen (esto puede ir en main o en test setup)
Base.metadata.create_all(bind=engine)
