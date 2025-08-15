# API Semana 2 - FastAPI

## ¿Qué hace?
API mínima para la Semana 2 del curso FastAPI, con:
- ✅ Type hints en todas las funciones
- ✅ Validación automática con Pydantic
- ✅ Endpoint POST y PATCH async
- ✅ Enums para estados
- ✅ Listas en memoria como almacenamiento

## Endpoints
- `POST /users` → Crear usuario
- `GET /users` → Listar usuarios
- `POST /tasks` → Crear tarea
- `PATCH /tasks/{id}/status` → Cambiar estado de tarea

## Cómo ejecutar
```bash
pip install fastapi pydantic uvicorn
uvicorn main:app --reload
