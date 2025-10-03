"""
Configuración de Fixtures - Lavandería Express QuickClean
ROJAS BURBANO - Ficha 3147246

Fixtures genéricas para testing de servicios de lavandería (Tipo C)
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from app.main import app
from app.database import get_db, Base

# Configuración de base de datos de prueba
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///./test_lavanderia.db"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test
)

fake = Faker("es_ES")  # Faker en español


@pytest.fixture(scope="session")
def event_loop():
    """Configuración del loop de eventos para tests async"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Fixture de sesión de base de datos para tests"""
    # Crear tablas
    Base.metadata.create_all(bind=engine_test)

    # Crear sesión
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        # Limpiar después de cada test
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="function")
def client(db_session):
    """Fixture de cliente de prueba de FastAPI"""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    """Fixture para headers de autenticación"""
    # Token genérico para tests
    return {"Authorization": "Bearer test_token_lavanderia"}


# ==================== FIXTURES TIPO C - SERVICIOS DE LAVANDERÍA ====================


@pytest.fixture
def sample_servicio_lavanderia():
    """Fixture para servicio de lavandería de prueba"""
    return {
        "nombre": f"Servicio {fake.word().title()}",
        "descripcion": fake.text(max_nb_chars=200),
        "tipo_servicio": fake.random_element(
            ["lavado_seco", "lavado_agua", "planchado", "tintoreria", "express"]
        ),
        "precio_base": round(fake.random.uniform(5000.0, 50000.0), 2),
        "tiempo_estimado_horas": fake.random_element([4, 24, 48, 72]),
        "activo": True,
    }


@pytest.fixture
def multiple_servicios_lavanderia():
    """Fixture para múltiples servicios de lavandería"""
    servicios = []
    tipos = ["lavado_seco", "lavado_agua", "planchado", "tintoreria", "express"]

    for i, tipo in enumerate(tipos):
        servicios.append(
            {
                "nombre": f"{tipo.replace('_', ' ').title()} Premium",
                "descripcion": f"Servicio especializado de {tipo}",
                "tipo_servicio": tipo,
                "precio_base": 10000.0 * (i + 1),
                "tiempo_estimado_horas": 24 * (i + 1),
                "activo": True,
            }
        )

    return servicios


@pytest.fixture
def sample_cliente_lavanderia():
    """Fixture para cliente de lavandería de prueba"""
    return {
        "nombre_completo": fake.name(),
        "email": fake.email(),
        "telefono": f"300{fake.random_number(digits=7)}",
        "direccion": fake.address(),
        "password": "password123",
        "preferencias": {
            "notificaciones_email": True,
            "notificaciones_sms": fake.boolean(),
            "servicio_favorito": "lavado_seco",
        },
    }


@pytest.fixture
def multiple_clientes_lavanderia():
    """Fixture para múltiples clientes"""
    return [
        {
            "nombre_completo": fake.name(),
            "email": fake.email(),
            "telefono": f"300{fake.random_number(digits=7)}",
            "direccion": fake.address(),
            "password": "password123",
        }
        for _ in range(5)
    ]


@pytest.fixture
def sample_orden_lavanderia():
    """Fixture para orden de lavandería de prueba"""
    return {
        "cliente_id": 1,
        "servicio_id": 1,
        "cantidad_prendas": fake.random_int(1, 20),
        "descripcion_prendas": f"{fake.random_int(1, 5)} camisas, {fake.random_int(1, 3)} pantalones",
        "prioridad": fake.random_element(["normal", "urgente", "express"]),
        "observaciones": fake.text(max_nb_chars=200),
    }


@pytest.fixture
def multiple_ordenes_lavanderia():
    """Fixture para múltiples órdenes"""
    return [
        {
            "cliente_id": 1,
            "servicio_id": i + 1,
            "cantidad_prendas": fake.random_int(3, 15),
            "descripcion_prendas": f"Orden {i+1}: {fake.text(max_nb_chars=50)}",
            "prioridad": "normal",
        }
        for i in range(3)
    ]


# ==================== FIXTURES DE UTILIDAD ====================


@pytest.fixture
def pagination_params():
    """Fixture para parámetros de paginación"""
    return {"skip": 0, "limit": 10, "sort_by": "id", "sort_order": "asc"}


@pytest.fixture
def search_params():
    """Fixture para parámetros de búsqueda"""
    return {
        "query": fake.word(),
        "filters": {"activo": True, "tipo_servicio": "lavado_seco"},
    }


@pytest.fixture
def sample_user_generic():
    """Fixture para usuario genérico de autenticación"""
    return {
        "username": "usuario_test_lavanderia",
        "email": "test@lavanderia.com",
        "password": "password123",
        "is_active": True,
    }


# ==================== FIXTURES PARA ESTADOS Y VALIDACIONES ====================


@pytest.fixture
def estados_orden_validos():
    """Fixture con estados válidos de órdenes"""
    return ["recibida", "en_proceso", "lista", "entregada", "cancelada"]


@pytest.fixture
def tipos_servicio_validos():
    """Fixture con tipos de servicio válidos"""
    return ["lavado_seco", "lavado_agua", "planchado", "tintoreria", "express"]


@pytest.fixture
def prioridades_validas():
    """Fixture con prioridades válidas"""
    return ["normal", "urgente", "express"]
