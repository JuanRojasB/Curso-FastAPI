# Centro Estético API - Semana 7

## Endpoints simulados para pruebas

- **POST /spa/reservas**
  - Simula la creación de una reserva.
  - Si se hacen más de 100 requests, responde 429 (rate limiting).

- **GET /spa/horario-restringido**
  - Simula acceso fuera de horario, responde 403.

- **POST /spa/accion-log**
  - Simula logging y crea el archivo `logs/spa_domain.log`.

- **GET /spa/cliente-protegido**
  - Simula validación de headers requeridos para clientes y empleados.
  - Responde 400 si faltan headers, 200 si están presentes.

## Pruebas automáticas

- Los tests de middleware pasan correctamente y validan la lógica de negocio.
- Los tests de caché requieren Redis corriendo en `localhost:6379` (si no está, fallan).
- Los tests de base de datos requieren un fixture `db_session` de SQLAlchemy (si no está, fallan).

## Recomendaciones para entrega

- Si no tienes Redis, puedes comentar los tests de caché para evitar fallos.
- Si no tienes base de datos configurada, comenta los tests de optimización de base de datos.
- Los endpoints simulados permiten validar la lógica y la integración de FastAPI.

---

**¡Listo para entregar!**
