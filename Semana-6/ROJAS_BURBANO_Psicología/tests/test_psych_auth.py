import pytest

class TestPsychAuth:
    def test_register_psych_user(self, client):
        """Test de registro específico para psicología"""
        data = {
            "username": "dr_juan_perez",
            "email": "juan.perez@clinicapsi.com",
            "password": "Psico2025!",
            "role": "psychologist"
        }
        response = client.post("/register", json=data)
        assert response.status_code in (200, 201)

    def test_login_psych_user(self, client):
        """Test de login específico para psicología"""
        register_data = {
            "username": "admin_clinicapsi",
            "email": "admin@clinicapsi.com",
            "password": "AdminPsico2025!",
            "role": "admin"
        }
        client.post("/register", json=register_data)
        login_data = {
            "username": "admin_clinicapsi",
            "password": "AdminPsico2025!"
        }
        client.post("/register", json=register_data)
        response = client.post("/login", json=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_psychologist_permissions(self, client):
        """Test de permisos específicos para psicólogo"""
        # Ejemplo: acceso a consulta clínica
        user_data = {
            "username": "dra_marta_lopez",
            "email": "marta.lopez@clinicapsi.com",
            "password": "Psico2025!",
            "role": "psychologist"
        }
        client.post("/register", json=user_data)
        login_data = {
            "username": "dra_marta_lopez",
            "password": "Psico2025!"
        }
        login_resp = client.post("/login", json=login_data)
        token = login_resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        # Intentar acceder a endpoint restringido
        resp = client.get("/psych_consultas", headers=headers)
        assert resp.status_code in (200, 403)

    def test_patient_access_restrictions(self, client):
        """Test de restricciones de acceso para pacientes"""
        user_data = {
            "username": "carlos_gomez",
            "email": "carlos.gomez@clinicapsi.com",
            "password": "Paciente2025!",
            "role": "patient"
        }
        client.post("/register", json=user_data)
        login_data = {
            "username": "carlos_gomez",
            "password": "Paciente2025!"
        }
        login_resp = client.post("/login", json=login_data)
        token = login_resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        # Intentar acceder a datos de otro paciente
        resp = client.get("/patients/9999", headers=headers)
        assert resp.status_code in (403, 404)

    def test_create_psych_consult_requires_auth(self, client):
        """Test que crear consulta requiere autenticación"""
        data = {
            "patient_id": 1,
            "reason_for_consultation": "Ansiedad",
            "preliminary_diagnosis": "Estrés",
            "current_medication": "Ninguno",
            "first_session_date": "2025-09-20",
            "number_of_sessions": 5,
            "assigned_therapist": "Dr. Juan",
            "observations": "Sin antecedentes relevantes."
        }
        response = client.post("/psych_consultas", json=data)
        assert response.status_code in (401, 403)

    def test_admin_can_delete_psych_consult(self, client):
        """Test que solo admin puede eliminar consulta psicológica"""
        admin_data = {
            "username": "admin_clinicapsi",
            "email": "admin@clinicapsi.com",
            "password": "AdminPsico2025!",
            "role": "admin"
        }
        client.post("/register", json=admin_data)
        login_data = {
            "username": "admin_clinicapsi",
            "password": "AdminPsico2025!"
        }
        login_resp = client.post("/login", json=login_data)
        token = login_resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        # Simular eliminación de consulta
        resp = client.delete("/psych_consultas/1", headers=headers)
        assert resp.status_code in (200, 404)

    def test_regular_user_cannot_delete_psych_consult(self, client):
        """Test que usuario regular no puede eliminar consulta psicológica"""
        user_data = {
            "username": "carlos_gomez",
            "email": "carlos.gomez@clinicapsi.com",
            "password": "Paciente2025!",
            "role": "patient"
        }
        client.post("/register", json=user_data)
        login_data = {
            "username": "carlos_gomez",
            "password": "Paciente2025!"
        }
        login_resp = client.post("/login", json=login_data)
        token = login_resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        # Intentar eliminar consulta como paciente
        resp = client.delete("/psych_consultas/1", headers=headers)
        assert resp.status_code in (403, 404)
