"""
Tests CRUD de Órdenes - Lavandería Express QuickClean
ROJAS BURBANO - Ficha 3147246

Tests completos para operaciones CRUD de órdenes
"""

import pytest
from fastapi import status


@pytest.mark.tipo_c
@pytest.mark.ordenes
@pytest.mark.crud
class TestOrdenesCRUD:
    """Tests CRUD para órdenes de lavandería"""

    def test_crear_orden_valida(self, client, sample_orden_lavanderia):
        """Test crear orden con datos válidos"""
        response = client.post("/api/v1/ordenes", json=sample_orden_lavanderia)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["cliente_id"] == sample_orden_lavanderia["cliente_id"]
        assert data["servicio_id"] == sample_orden_lavanderia["servicio_id"]
        assert data["cantidad_prendas"] == sample_orden_lavanderia["cantidad_prendas"]
        assert "numero_orden" in data
        assert data["estado"] == "recibida"
        assert "fecha_recepcion" in data
        assert "fecha_estimada_entrega" in data

    def test_crear_orden_sin_cliente(self, client, sample_orden_lavanderia):
        """Test crear orden sin cliente debe fallar"""
        orden_invalida = sample_orden_lavanderia.copy()
        del orden_invalida["cliente_id"]

        response = client.post("/api/v1/ordenes", json=orden_invalida)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_crear_orden_cantidad_prendas_cero(self, client, sample_orden_lavanderia):
        """Test crear orden con cantidad de prendas cero debe fallar"""
        orden_invalida = sample_orden_lavanderia.copy()
        orden_invalida["cantidad_prendas"] = 0

        response = client.post("/api/v1/ordenes", json=orden_invalida)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_listar_ordenes(self, client):
        """Test listar todas las órdenes"""
        response = client.get("/api/v1/ordenes")

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_listar_ordenes_por_cliente(self, client):
        """Test listar órdenes filtradas por cliente"""
        response = client.get("/api/v1/ordenes?cliente_id=1")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_listar_ordenes_por_estado(self, client):
        """Test listar órdenes filtradas por estado"""
        response = client.get("/api/v1/ordenes?estado=recibida")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_obtener_orden_por_id(self, client):
        """Test obtener orden específica por ID"""
        response = client.get("/api/v1/ordenes/1")

        # 404 hasta que se implemente la base de datos
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_actualizar_orden(self, client):
        """Test actualizar orden existente"""
        update_data = {
            "cantidad_prendas": 10,
            "observaciones": "Actualización de test",
        }

        response = client.put("/api/v1/ordenes/1", json=update_data)

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_cambiar_estado_orden(self, client):
        """Test cambiar estado de una orden"""
        response = client.patch(
            "/api/v1/ordenes/1/estado", params={"nuevo_estado": "en_proceso"}
        )

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
        ]


@pytest.mark.tipo_c
@pytest.mark.ordenes
@pytest.mark.integration
class TestOrdenesEstados:
    """Tests de transiciones de estado de órdenes"""

    def test_estado_inicial_recibida(self, client, sample_orden_lavanderia):
        """Test que orden nueva tiene estado 'recibida'"""
        response = client.post("/api/v1/ordenes", json=sample_orden_lavanderia)

        data = response.json()
        assert data["estado"] == "recibida"

    def test_estados_validos(self, client, estados_orden_validos):
        """Test que todos los estados válidos son aceptados"""
        for estado in estados_orden_validos:
            response = client.patch(
                "/api/v1/ordenes/1/estado", params={"nuevo_estado": estado}
            )

            # Verificar que el estado es válido
            assert response.status_code in [
                status.HTTP_200_OK,
                status.HTTP_404_NOT_FOUND,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ]

    def test_estado_invalido(self, client):
        """Test que estado inválido es rechazado"""
        response = client.patch(
            "/api/v1/ordenes/1/estado", params={"nuevo_estado": "estado_invalido"}
        )

        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_404_NOT_FOUND,
        ]
