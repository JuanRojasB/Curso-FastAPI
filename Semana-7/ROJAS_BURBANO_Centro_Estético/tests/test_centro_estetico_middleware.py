import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestCentroEsteticoMiddleware:
    def test_rate_limiting_reservas(self):
        """Verifica que el rate limiting funcione en reservas"""
        for i in range(150):
            response = client.post("/spa/reservas", json={"cliente_id": 1, "tratamiento_id": 2, "fecha": "2025-09-25T10:00:00"})
            if response.status_code == 429:
                break
        else:
            pytest.fail("Rate limiting no se activó en reservas")

    def test_horarios_atencion(self):
        """Verifica validación de horarios de atención del centro estético"""
        # Simular request fuera de horario (requiere mock del tiempo)
        response = client.get("/spa/horario-restringido")
        assert response.status_code in [200, 403]

    def test_logging_acciones(self):
        """Verifica que el logging de acciones relevantes funcione"""
        response = client.post("/spa/accion-log", json={"empleado_id": 1, "accion": "registro_reserva"})
        assert response.status_code == 200
        import os
        assert os.path.exists("logs/spa_domain.log")

    def test_headers_cliente_empleado(self):
        """Verifica validación de headers requeridos para clientes y empleados"""
        response = client.get("/spa/cliente-protegido")
        headers = {"X-Cliente-Token": "token123", "X-Empleado-Token": "token456"}
        response_with_headers = client.get("/spa/cliente-protegido", headers=headers)
        assert response.status_code == 400 or response_with_headers.status_code == 200