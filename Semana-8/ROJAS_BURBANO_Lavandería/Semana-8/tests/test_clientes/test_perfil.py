"""
Tests de Perfil de Cliente - Lavandería Express QuickClean
ROJAS BURBANO - Ficha 3147246

Tests para gestión de perfiles de clientes
"""

import pytest
from fastapi import status


@pytest.mark.tipo_c
@pytest.mark.clientes
@pytest.mark.integration
class TestClientesPerfil:
    """Tests de gestión de perfiles de clientes"""

    def test_registrar_cliente_valido(self, client, sample_cliente_lavanderia):
        """Test registrar cliente con datos válidos"""
        response = client.post("/api/v1/clientes", json=sample_cliente_lavanderia)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nombre_completo"] == sample_cliente_lavanderia["nombre_completo"]
        assert data["email"] == sample_cliente_lavanderia["email"]
        assert data["telefono"] == sample_cliente_lavanderia["telefono"]
        assert "id" in data
        assert data["activo"] is True
        assert "password" not in data  # No debe retornar la contraseña

    def test_registrar_cliente_email_invalido(self, client, sample_cliente_lavanderia):
        """Test registrar cliente con email inválido debe fallar"""
        cliente_invalido = sample_cliente_lavanderia.copy()
        cliente_invalido["email"] = "email_invalido"

        response = client.post("/api/v1/clientes", json=cliente_invalido)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_registrar_cliente_telefono_invalido(
        self, client, sample_cliente_lavanderia
    ):
        """Test registrar cliente con teléfono inválido debe fallar"""
        cliente_invalido = sample_cliente_lavanderia.copy()
        cliente_invalido["telefono"] = "12345"  # Formato inválido

        response = client.post("/api/v1/clientes", json=cliente_invalido)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_listar_clientes(self, client):
        """Test listar todos los clientes"""
        response = client.get("/api/v1/clientes")

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_listar_clientes_activos(self, client):
        """Test listar solo clientes activos"""
        response = client.get("/api/v1/clientes?activo=true")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_obtener_cliente_por_id(self, client):
        """Test obtener cliente específico por ID"""
        response = client.get("/api/v1/clientes/1")

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_actualizar_cliente(self, client):
        """Test actualizar información de cliente"""
        update_data = {
            "nombre_completo": "Cliente Actualizado",
            "telefono": "3009876543",
        }

        response = client.put("/api/v1/clientes/1", json=update_data)

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_desactivar_cliente(self, client):
        """Test desactivar cliente (soft delete)"""
        response = client.delete("/api/v1/clientes/1")

        assert response.status_code in [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_cliente_preferencias(self, client, sample_cliente_lavanderia):
        """Test que preferencias del cliente se guardan correctamente"""
        cliente_con_preferencias = sample_cliente_lavanderia.copy()
        cliente_con_preferencias["preferencias"] = {
            "notificaciones_email": True,
            "notificaciones_sms": False,
            "servicio_favorito": "lavado_seco",
        }

        response = client.post("/api/v1/clientes", json=cliente_con_preferencias)

        data = response.json()
        assert "preferencias" in data
        assert data["preferencias"]["notificaciones_email"] is True
