from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any

class DomainOptimizedQueries:
    """Consultas optimizadas específicas para tu dominio"""

    @staticmethod
    def get_optimized_queries_type_a():
        """Consultas optimizadas para dominios tipo A (entidades con historiales)"""
        return {
            'historial_entidad': """
                SELECT h.*, r.nombre as responsable_nombre
                FROM historiales h
                JOIN responsables r ON h.responsable_id = r.id
                WHERE h.entidad_id = :entidad_id
                ORDER BY h.fecha_registro DESC
                LIMIT :limit
            """,
            'proximos_vencimientos': """
                SELECT e.nombre, tv.descripcion,
                       (r.fecha_aplicacion + tv.duracion_dias * INTERVAL '1 day') as proxima_fecha
                FROM entidades e
                JOIN registros r ON e.id = r.entidad_id
                JOIN tipos_registro tv ON r.tipo_id = tv.id
                WHERE e.propietario_id = :propietario_id
                AND (r.fecha_aplicacion + tv.duracion_dias * INTERVAL '1 day') <= CURRENT_DATE + INTERVAL '30 days'
            """
        }

    @staticmethod
    def get_optimized_queries_type_b():
        """Consultas optimizadas para dominios tipo B (horarios y disponibilidad)"""
        return {
            'recursos_disponibles': """
                SELECT r.nombre, e.dia_semana, e.hora_inicio, e.hora_fin
                FROM recursos r
                LEFT JOIN eventos e ON r.id = e.recurso_id
                    AND e.dia_semana = :dia
                    AND e.hora_inicio = :hora
                WHERE r.disponible = true
                AND r.capacidad >= :capacidad_minima
                AND e.id IS NULL
                ORDER BY r.capacidad
            """,
            'reservas_usuario': """
                SELECT e.nombre, e.dia_semana, e.hora_inicio,
                       resp.nombre as responsable, r.nombre as recurso
                FROM reservas res
                JOIN eventos e ON res.evento_id = e.id
                JOIN responsables resp ON e.responsable_id = resp.id
                JOIN recursos r ON e.recurso_id = r.id
                WHERE res.usuario_id = :usuario_id
                AND res.estado = 'activa'
                ORDER BY e.dia_semana, e.hora_inicio
            """
        }

    @staticmethod
    def get_optimized_queries_type_c():
        """Consultas optimizadas para dominios tipo C (usuarios y asignaciones)"""
        return {
            'asignacion_activa_usuario': """
                SELECT a.nombre, el.nombre as elemento, ae.cantidad, ae.parametros
                FROM asignaciones_usuario au
                JOIN asignaciones a ON au.asignacion_id = a.id
                JOIN asignacion_elementos ae ON a.id = ae.asignacion_id
                JOIN elementos el ON ae.elemento_id = el.id
                WHERE au.usuario_id = :usuario_id
                AND au.activa = true
                ORDER BY ae.orden
            """,
            'recursos_disponibles_usuario': """
                SELECT r.nombre, r.descripcion,
                       CASE WHEN uso.recurso_id IS NULL THEN true ELSE false END as disponible
                FROM recursos r
                LEFT JOIN uso_recursos uso ON r.id = uso.recurso_id
                    AND uso.fecha_uso = CURRENT_DATE
                    AND uso.activo = true
                WHERE r.mantenimiento = false
                ORDER BY r.popularidad DESC
            """
        }

    @staticmethod
    def get_optimized_queries_type_d():
        """Consultas optimizadas para dominios tipo D (productos e inventario)"""
        return {
            'productos_disponibles': """
                SELECT p.nombre, p.descripcion, p.precio,
                       i.stock_actual, prov.nombre as proveedor
                FROM productos p
                JOIN inventario i ON p.id = i.producto_id
                JOIN proveedores prov ON p.proveedor_id = prov.id
                WHERE i.stock_actual > :stock_minimo
                AND p.disponible = true
                AND (:buscar IS NULL OR
                     p.nombre ILIKE '%' || :buscar || '%' OR
                     p.descripcion ILIKE '%' || :buscar || '%')
                ORDER BY p.nombre
            """,
            'alertas_stock_bajo': """
                SELECT p.nombre, i.stock_actual, i.stock_minimo,
                       (i.stock_actual::float / i.stock_minimo) as ratio_stock
                FROM productos p
                JOIN inventario i ON p.id = i.producto_id
                WHERE i.stock_actual <= i.stock_minimo * 1.2
                AND p.disponible = true
                ORDER BY ratio_stock ASC
            """
        }

    @staticmethod
    def get_queries_for_domain(domain_type: str):
        """
        Obtiene consultas optimizadas según el tipo de dominio
        DEBES analizar TU dominio y elegir el tipo más apropiado
        """
        if domain_type == "type_a":
            return DomainOptimizedQueries.get_optimized_queries_type_a()
        elif domain_type == "type_b":
            return DomainOptimizedQueries.get_optimized_queries_type_b()
        elif domain_type == "type_c":
            return DomainOptimizedQueries.get_optimized_queries_type_c()
        elif domain_type == "type_d":
            return DomainOptimizedQueries.get_optimized_queries_type_d()
        else:
            return {}