class TestPsychologyAPI:

    def test_create_consult_success(self, client, auth_headers, sample_patient_data, sample_psychology_consult_data):
        # 1) Create patient first
        patient_resp = client.post("/patients", json=sample_patient_data, headers=auth_headers)
        assert patient_resp.status_code == 200
        patient_id = patient_resp.json()["id"]

        # 2) Prepare consultation data with patient_id
        consult_data = sample_psychology_consult_data.copy()
        consult_data["patient_id"] = patient_id

        # 3) Create consultation
        response = client.post("/psych_consultas", json=consult_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()

        # Validate returned fields
        assert data["patient_id"] == patient_id
        assert data["reason_for_consultation"] == consult_data["reason_for_consultation"]
        assert data["preliminary_diagnosis"] == consult_data["preliminary_diagnosis"]
        assert data["current_medication"] == consult_data["current_medication"]
        assert data["first_session_date"] == consult_data["first_session_date"]
        assert data["number_of_sessions"] == consult_data["number_of_sessions"]
        assert data["assigned_therapist"] == consult_data["assigned_therapist"]
        assert data["observations"] == consult_data["observations"]

    def test_get_consult_not_found(self, client, auth_headers):
        response = client.get("/psych_consultas/9999", headers=auth_headers)
        assert response.status_code == 404
        assert "Not Found" in response.json()["detail"]

    def test_consult_validation_error(self, client, auth_headers):
        # Validation errors: missing required fields or invalid values
        invalid_data = {
            # patient_id is required but missing
            "reason_for_consultation": "",     # required, empty string invalid
            "number_of_sessions": -1,          # invalid negative
            "first_session_date": "invalid-date"  # invalid date format
        }
        response = client.post(
            "/psych_consultas",
            json=invalid_data,
            headers=auth_headers
        )
        assert response.status_code == 422
        errors = response.json()["detail"]

        # Validate errors include the expected fields
        assert any("reason_for_consultation" in str(error) for error in errors)
        assert any("patient_id" in str(error) for error in errors)
        assert any("number_of_sessions" in str(error) for error in errors)
        assert any("first_session_date" in str(error) for error in errors)

    # Tests de Consulta (GET)

    
    def test_create_psych_complete(self, client, auth_headers):
        # Datos de ejemplo para una consulta psicológica (ajustar según tu dominio)
        data = {
            "patient_id": 123,  # ID de un paciente existente
            "reason_for_consultation": "Ansiedad",  # Ejemplo de motivo de consulta
            "preliminary_diagnosis": "Estrés generalizado",  # Diagnóstico preliminar
            "current_medication": "Ninguno",  # Medicación actual
            "first_session_date": "2023-09-15",  # Fecha de la primera sesión
            "number_of_sessions": 10,  # Número de sesiones recomendadas
            "assigned_therapist": "Dr. Juan Pérez",  # Nombre del terapeuta asignado
            "observations": "Paciente con antecedentes de ansiedad."  # Observaciones relevantes
        }

        # Enviar la solicitud para crear la consulta
        response = client.post(f"/psych_consultas/", json=data, headers=auth_headers)

        # Verificar que la respuesta tiene código 201 (creación exitosa)
        assert response.status_code == 201
        
        # Obtener la respuesta en formato JSON
        created = response.json()

        # Validaciones específicas
        assert created["patient_id"] == data["patient_id"]
        assert created["reason_for_consultation"] == data["reason_for_consultation"]
        assert created["preliminary_diagnosis"] == data["preliminary_diagnosis"]
        assert created["current_medication"] == data["current_medication"]
        assert created["first_session_date"] == data["first_session_date"]
        assert created["number_of_sessions"] == data["number_of_sessions"]
        assert created["assigned_therapist"] == data["assigned_therapist"]
        assert created["observations"] == data["observations"]
        assert "id" in created  # Verificar que la consulta creada tiene un ID único
        
        
    def test_update_consulta_complete(self, client, auth_headers):
        # Test de actualización completa para Psicología
        
        # Crear la consulta inicial con datos de un usuario específico
        create_data = {
            "patient_id": 456,  # ID de un paciente existente
            "reason_for_consultation": "Ansiedad",  # Motivo inicial de consulta
            "preliminary_diagnosis": "Estrés generalizado",  # Diagnóstico inicial
            "current_medication": "Ninguno",  # Medicación inicial
            "first_session_date": "2023-09-15",  # Fecha de la primera sesión inicial
            "number_of_sessions": 10,  # Número de sesiones inicial
            "assigned_therapist": "Dr. Juan Pérez",  # Terapeuta asignado inicial
            "observations": "Paciente con antecedentes de ansiedad."  # Observaciones iniciales
        }
        
        # Crear la consulta (POST)
        create_response = client.post(f"/psych_consultas/", json=create_data, headers=auth_headers)
        assert create_response.status_code == 201
        entity_id = create_response.json()["id"]  # Obtener el ID de la consulta creada
        
        # Datos de actualización completa con un nuevo ID para el ejemplo
        update_data = {
            "patient_id": 456,  # ID del paciente
            "reason_for_consultation": "Depresión",  # Nuevo motivo de consulta
            "preliminary_diagnosis": "Depresión mayor",  # Nuevo diagnóstico preliminar
            "current_medication": "Antidepresivos",  # Nueva medicación
            "first_session_date": "2023-09-20",  # Nueva fecha de la primera sesión
            "number_of_sessions": 12,  # Nuevo número de sesiones
            "assigned_therapist": "Dra. Marta López",  # Nuevo terapeuta asignado
            "observations": "Paciente con antecedentes familiares de depresión."  # Nueva observación
        }
        
        # Realizar la actualización completa (PUT)
        response = client.put(f"/psych_consultas/{entity_id}", json=update_data, headers=auth_headers)
        
        # Verificar la respuesta (debe ser código 200)
        assert response.status_code == 200
        updated = response.json()  # Obtener los datos de la consulta actualizada
        
        # Validar que los datos se hayan actualizado correctamente
        assert updated["patient_id"] == update_data["patient_id"]
        assert updated["reason_for_consultation"] == update_data["reason_for_consultation"]
        assert updated["preliminary_diagnosis"] == update_data["preliminary_diagnosis"]
        assert updated["current_medication"] == update_data["current_medication"]
        assert updated["first_session_date"] == update_data["first_session_date"]
        assert updated["number_of_sessions"] == update_data["number_of_sessions"]
        assert updated["assigned_therapist"] == update_data["assigned_therapist"]
        assert updated["observations"] == update_data["observations"]


    def test_update_consulta_partial(self, client, auth_headers):
        # Test de actualización parcial para Psicología
        
        # Crear la consulta inicial con datos de otro usuario específico
        create_data = {
            "patient_id": 789,  # ID de un paciente diferente
            "reason_for_consultation": "Estrés",  # Motivo inicial de consulta
            "preliminary_diagnosis": "Estrés generalizado",  # Diagnóstico inicial
            "current_medication": "Ninguno",  # Medicación inicial
            "first_session_date": "2023-09-25",  # Fecha de la primera sesión inicial
            "number_of_sessions": 8,  # Número de sesiones inicial
            "assigned_therapist": "Dr. Luis Gómez",  # Terapeuta asignado inicial
            "observations": "Paciente con alta carga laboral."  # Observaciones iniciales
        }
        
        # Crear la consulta (POST)
        create_response = client.post(f"/psych_consultas/", json=create_data, headers=auth_headers)
        assert create_response.status_code == 201
        entity_id = create_response.json()["id"]  # Obtener el ID de la consulta creada
        
        # Datos de actualización parcial
        partial_update_data = {
            "current_medication": "Ansiolíticos",  # Solo se actualiza la medicación
            "assigned_therapist": "Dra. Paula Torres",  # Solo se actualiza el terapeuta
        }
        
        # Realizar la actualización parcial (PATCH)
        response = client.patch(f"/psych_consultas/{entity_id}", json=partial_update_data, headers=auth_headers)
        
        # Verificar la respuesta (debe ser código 200)
        assert response.status_code == 200
        updated = response.json()  # Obtener los datos de la consulta actualizada
        
        # Validar que los datos se hayan actualizado correctamente solo en los campos modificados
        assert updated["current_medication"] == partial_update_data["current_medication"]
        assert updated["assigned_therapist"] == partial_update_data["assigned_therapist"]
        
        # Verificar que los demás campos no se hayan modificado
        assert updated["reason_for_consultation"] == create_data["reason_for_consultation"]
        assert updated["preliminary_diagnosis"] == create_data["preliminary_diagnosis"]
        assert updated["first_session_date"] == create_data["first_session_date"]
        assert updated["number_of_sessions"] == create_data["number_of_sessions"]
        assert updated["observations"] == create_data["observations"]

    # Tests de Eliminación (DELETE)

    def test_delete_psych_consult_success(self, client, auth_headers):
        """Test de eliminación exitosa en psicología"""
        # Crear la consulta
        create_data = {
            "patient_id": 123,  # ID de un paciente existente
            "reason_for_consultation": "Ansiedad",
            "preliminary_diagnosis": "Estrés generalizado",
            "current_medication": "Ninguno",
            "first_session_date": "2023-09-15",
            "number_of_sessions": 10,
            "assigned_therapist": "Dr. Juan Pérez",
            "observations": "Paciente con antecedentes de ansiedad."
        }

        # Crear la consulta (POST)
        create_response = client.post("/psych_consultas", json=create_data, headers=auth_headers)
        assert create_response.status_code == 201
        entity_id = create_response.json()["id"]  # Obtener el ID de la consulta creada

        # Eliminar la consulta (DELETE)
        delete_response = client.delete(f"/psych_consultas/{entity_id}", headers=auth_headers)
        assert delete_response.status_code == 200  # La eliminación debe ser exitosa

        # Verificar que la consulta ya no existe
        get_response = client.get(f"/psych_consultas/{entity_id}", headers=auth_headers)
        assert get_response.status_code == 404  # Debería devolver un 404 porque la consulta fue eliminada

    def test_delete_psych_consult_not_found(self, client, auth_headers):
        """Test de eliminación de entidad inexistente en psicología"""
        # Intentar eliminar una consulta que no existe
        response = client.delete("/psych_consultas/99999", headers=auth_headers)  # ID ficticio
        assert response.status_code == 404  # Debería devolver un 404 porque la consulta no existe
