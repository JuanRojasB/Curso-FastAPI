# app/database/indexes.py
from sqlalchemy import Index, text
from app.database import engine

class DomainIndexes:
    """Índices específicos para optimizar consultas de tu dominio"""

    @staticmethod
    def create_domain_type_a_indexes():
        """Índices para dominios tipo A (entidad principal con historiales)"""
        indexes = [
            # Búsquedas frecuentes por entidad principal
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_entidad_propietario ON entidades_principales(propietario_id, activa);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_historial_entidad_fecha ON historiales(entidad_id, fecha_registro DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_citas_responsable_fecha ON citas(responsable_id, fecha_cita, estado);",
            # Búsquedas por tipo y categoría
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_registros_entidad_tipo ON registros(entidad_id, tipo_registro, fecha_aplicacion DESC);",
        ]
        return indexes

    @staticmethod
    def create_domain_type_b_indexes():
        """Índices para dominios tipo B (horarios y disponibilidad)"""
        indexes = [
            # Consultas de horarios y disponibilidad
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_eventos_horario ON eventos(dia_semana, hora_inicio, recurso_id);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reservas_usuario ON reservas(usuario_id, estado, fecha_reserva DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_recursos_disponibilidad ON recursos(disponible, capacidad, tipo_recurso);",
            # Búsquedas por responsable
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_eventos_responsable_fecha ON eventos(responsable_id, fecha_evento, estado);",
        ]
        return indexes

    @staticmethod
    def create_domain_type_c_indexes():
        """Índices para dominios tipo C (usuarios y asignaciones)"""
        indexes = [
            # Consultas de asignaciones y perfiles
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_asignaciones_usuario ON asignaciones_usuario(usuario_id, activa, fecha_creacion DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_perfiles_usuario_estado ON perfiles(usuario_id, estado, fecha_vencimiento);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_elementos_tipo_categoria ON elementos(tipo_elemento, categoria);",
            # Actividades y uso
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_actividades_usuario_fecha ON actividades(usuario_id, fecha_actividad DESC);",
        ]
        return indexes

    @staticmethod
    def create_domain_type_d_indexes():
        """Índices para dominios tipo D (productos y stock)"""
        indexes = [
            # Búsquedas de productos y stock
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_productos_nombre_disponible ON productos(nombre, descripcion, disponible);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_inventario_producto_stock ON inventario(producto_id, stock_actual, fecha_actualizacion DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_transacciones_fecha_total ON transacciones(fecha_transaccion DESC, total);",
            # Búsquedas por proveedor y categoría
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_productos_proveedor_categoria ON productos(proveedor_id, categoria_id, precio);",
        ]
        return indexes

    @staticmethod
    def get_domain_indexes(domain_type: str):
        """
        Obtiene índices específicos según el tipo de dominio
        DEBES analizar TU dominio y elegir el tipo más apropiado
        """
        if domain_type == "type_a":  # Entidades con historiales
            return DomainIndexes.create_domain_type_a_indexes()
        elif domain_type == "type_b":  # Horarios y disponibilidad
            return DomainIndexes.create_domain_type_b_indexes()
        elif domain_type == "type_c":  # Usuarios y asignaciones
            return DomainIndexes.create_domain_type_c_indexes()
        elif domain_type == "type_d":  # Productos e inventario
            return DomainIndexes.create_domain_type_d_indexes()
        else:
            # Índices genéricos básicos
            return [
                "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_entidad_principal_usuario ON entidad_principal(usuario_id, fecha_creacion DESC);",
                "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_entidad_principal_estado ON entidad_principal(estado, fecha_actualizacion);",
            ]

    @staticmethod
    async def create_indexes_for_domain(domain_prefix: str):
        """Crea índices específicos para tu dominio"""
        indexes = DomainIndexes.get_domain_indexes(domain_prefix)

        with engine.connect() as connection:
            for index_sql in indexes:
                try:
                    connection.execute(text(index_sql))
                    print(f"✅ Índice creado: {index_sql[:50]}...")
                except Exception as e:
                    print(f"❌ Error creando índice: {e}")