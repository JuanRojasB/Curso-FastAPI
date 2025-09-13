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
        response = client.post("/consultations", json=consult_data, headers=auth_headers)
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
        response = client.get("/consultations/9999", headers=auth_headers)
        assert response.status_code == 404
        assert "Consult not found" in response.json()["detail"]

    def test_consult_validation_error(self, client, auth_headers):
        # Validation errors: missing required fields or invalid values
        invalid_data = {
            # patient_id is required but missing
            "reason_for_consultation": "",     # required, empty string invalid
            "number_of_sessions": -1,          # invalid negative
            "first_session_date": "invalid-date"  # invalid date format
        }
        response = client.post(
            "/consultations",
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
