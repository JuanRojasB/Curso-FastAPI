import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base, engine

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./psych_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    # Create all tables declared in Base, including users, etc.
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Sample data fixture for patient (necessary to create before consult)
@pytest.fixture
def sample_patient_data():
    return {
        "first_name": "Lucía",
        "last_name": "Fernández López",
        "age": 29,
        "phone_number": "3001234567",
        "email": "lucia.fernandez@example.com",
        "medical_history": "No prior psychiatric history",
        "emergency_contact": "3007654321"
    }

# Sample data fixture for psychology consult (adapted)
@pytest.fixture
def sample_psychology_consult_data():
    return {
        "reason_for_consultation": "Generalized anxiety and difficulty sleeping",
        "preliminary_diagnosis": "Generalized Anxiety Disorder (F41.1)",
        "current_medication": "None",
        "first_session_date": "2025-09-01",
        "number_of_sessions": 4,
        "assigned_therapist": "Dr. Andrea Gómez",
        "observations": "Good treatment compliance. Psychiatric evaluation recommended if symptoms persist."
    }

@pytest.fixture
def auth_headers(client):
    # Register admin psychologist user for tests
    register_response = client.post("/register", json={
        "username": "admin_psych_",
        "email": "admin_psych@example.com",
        "password": "test123",
        "role": "psychologist"
    })
    assert register_response.status_code in (200, 400)  # allow already exists

    # Login to get token
    login_response = client.post("/login", json={
        "username": "admin_psych_",
        "password": "test123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
