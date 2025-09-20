import pytest



import pytest

def test_validacion_clinica_psych(client, auth_headers):
    """Cobertura de validaciones clínicas: datos obligatorios y formatos válidos"""
    invalid_data = {
        "reason_for_consultation": "",  # Vacío
        "number_of_sessions": -5,        # Negativo
        "first_session_date": "fecha-incorrecta"  # Formato inválido
    }
    response = client.post("/psych_consultas", json=invalid_data, headers=auth_headers)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("reason_for_consultation" in str(error) for error in errors)
    assert any("number_of_sessions" in str(error) for error in errors)
    assert any("first_session_date" in str(error) for error in errors)

def test_seguridad_datos_psych(client, auth_headers):
    """Cobertura de seguridad de datos: acceso restringido y protección de información"""
    # Intentar acceder sin autenticación
    response = client.get("/psych_consultas/1")
    assert response.status_code in (401, 403)

def test_ruta_critica_eliminacion_psych(client, auth_headers):
    """Cobertura de ruta crítica: eliminación y verificación de no existencia"""
    # Crear paciente válido primero
    patient_data = {
        "first_name": "Paciente",
        "last_name": "Test",
        "age": 30,
        "phone_number": "1234567890",
        "email": "paciente_test@example.com",
        "medical_history": "Sin antecedentes",
        "emergency_contact": "Contacto Test"
    }
    patient_resp = client.post("/patients", json=patient_data, headers=auth_headers)
    assert patient_resp.status_code == 200
    patient_id = patient_resp.json()["id"]

    # Crear consulta válida con patient_id
    from datetime import date
    data = {
        "patient_id": patient_id,
        "reason_for_consultation": "Estrés",
        "preliminary_diagnosis": "Estrés laboral",
        "current_medication": "Ninguno",
        "first_session_date": date.today().isoformat(),
        "number_of_sessions": 5,
        "assigned_therapist": "Dr. Juan",
        "observations": "Sin antecedentes relevantes."
    }
    create_resp = client.post("/psych_consultas", json=data, headers=auth_headers)
    assert create_resp.status_code == 201
    entity_id = create_resp.json()["id"]
    # Eliminar
    delete_resp = client.delete(f"/psych_consultas/{entity_id}", headers=auth_headers)
    assert delete_resp.status_code == 200
    # Verificar que no existe
    get_resp = client.get(f"/psych_consultas/{entity_id}", headers=auth_headers)
    assert get_resp.status_code == 404
