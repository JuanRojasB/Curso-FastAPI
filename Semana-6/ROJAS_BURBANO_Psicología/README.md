# Testing personalizado - Psicología (FICHA 3147246)

## Dominio: Psicología Clínica
- Entidad Principal: Paciente y Consulta Psicológica
- Prefijo Test: psych
- Módulo Test: ROJAS_BURBANO_Psicología

## Estructura y configuración

- `pytest.ini` con configuración estricta y markers personalizados
- `requirements.txt` actualizado con dependencias de testing
- `tests/conftest.py` con fixtures y datos realistas de psicología
- Tests específicos en `tests/test_psych_coverage.py` y `tests/test_psych_auth.py`
- Documentación de roles y casos de prueba en `docs/roles_psych.md` y `docs/testing_report_psych.md`

## Ejecución de tests

```bash
pytest tests/test_psych_coverage.py -v
pytest tests/test_psych_auth.py -v
```

## Ejemplo de fixture personalizada

```python
# tests/conftest.py
@pytest.fixture
def sample_patient_data():
    return {
        "first_name": "Roberto",
        "last_name": "Juan Perez",
        "age": 34,
        "phone_number": "3216549870",
        "email": "r_juan_perez@clinicapsi.com",
        "medical_history": "Ansiedad leve en 2023",
        "emergency_contact": "Maria Perez 3121234567"
    }
```


## Documentación Final y Verificación

### Entregables Semana 6 - FICHA 3147246

- Configuración personalizada de pytest (`pytest.ini`)
- Fixtures y datos realistas en `tests/conftest.py`
- Tests específicos en `tests/test_psych_coverage.py`, `tests/test_psych_auth.py`, `tests/test_psych_.py`
- Documentación de roles y KPIs en `docs/roles_psych.md` y `docs/testing_report_psych.md`
- Reporte de cobertura HTML en `htmlcov/index.html`
- `requirements.txt` actualizado

### Ejecución y verificación

```bash
pytest --cov=ROJAS_BURBANO_Psicología --cov-report=html --cov-report=term tests/ -v
```

- Todos los tests deben pasar sin errores
- Cobertura en módulos de pruebas: 100%
- Datos y lógica adaptados solo a psicología clínica
- No hay ejemplos genéricos ni duplicados

### Capturas y log de ejecución

- Incluye capturas de pantalla del resultado de pytest y cobertura
- Adjunta el reporte HTML generado (`htmlcov/index.html`)

### Reglas de oro para entrega

- Todos los nombres y datos son específicos de tu dominio
- La estructura y organización es profesional
- La documentación explica claramente el contexto y los casos de prueba
- Portfolio único y diferenciado para la FICHA 3147246

---
**¡Entrega lista para revisión y presentación profesional!**
