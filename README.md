# 🌐 Proyecto FastAPI - Bootcamp
👨‍💻 Estudiante: Juan David Rojas Burbano 
✉️ Contacto: juan.david.rojas.burbano0@gmail.com
📌 Inicio del proyecto: 02/08/2025  

---

## ⚙️ Preparación del Entorno

Este proyecto está pensado para ejecutarse en un entorno virtual independiente, lo que evita conflictos y facilita la colaboración.

- Carpeta del entorno: `venv-personal/`  
- Git configurado solo para este repositorio  
- Dependencias aisladas para no afectar otros proyectos

---

## ⚡ Cómo Ejecutar el Proyecto

```bash
# 1. Activar el entorno virtual
source venv-personal/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar servidor en modo desarrollo
uvicorn main:app --reload --port 8000
```

---

# 👉 Accede a la documentación interactiva en:
http://127.0.0.1:8000/docs

---

## 📚 Aprendizajes

### ✅ Semana 1 - Introducción
- Creación de la primera API con **FastAPI**.  
- Uso de **uvicorn** para ejecutar el servidor localmente.  
- Configuración inicial del repositorio y README básico.

### ✅ Semana 2 - Validación y Mejora
- Aplicación de **type hints** para mayor claridad y mantenimiento del código.  
- Validación automática de entradas con **Pydantic**, evitando datos inválidos.  
- Endpoints con **parámetros dinámicos** (`/products/{id}`) y **consultas** (`/search?name=...`).  
- Documentación automática con Swagger disponible en `/docs`.

### ✅ Semana 3 - Organización y buenas prácticas
- Reestructuración del proyecto en capas (por ejemplo: `models/`, `routers/`, `services/`) para separar responsabilidades.  
- Uso de **routers** para organizar endpoints y **services** para la lógica de negocio.  
- Implementación de endpoints **async** donde corresponda (simulación I/O), y manejo básico de errores con `HTTPException`.  
- Definición de **response models** para respuestas consistentes y uso apropiado de códigos HTTP.  
- Introducción a tests básicos y a consideraciones de paginación/filtrado para listados.

### ✅ Semana 4 - Bases de Datos con FastAPI

- Integración de SQLAlchemy con FastAPI para persistencia real en base de datos SQLite.
- Diseño de modelos relacionales simples con claves foráneas (One-to-Many).
- Implementación de CRUD completo para múltiples entidades (Create, Read, Update, Delete).
- Aplicación de validaciones de reglas de negocio básicas en los modelos.
- Realización de testing básico para verificar el correcto funcionamiento con bases de datos en memoria.
- Uso de migraciones con Alembic para gestionar cambios en el esquema de la base de datos.

### ✅ Semana 5 - Profundización en Prácticas

- Creación de proyectos más complejos con FastAPI aplicando la lógica aprendida.

- Uso de entornos virtuales y dependencias (requirements.txt).

- Estructuración de prácticas con distintos enfoques para afianzar conceptos.

- Trabajo en múltiples directorios de código, reforzando modularidad.

### ✅ Semana 6 - Proyecto Psicología

- Construcción de una API para gestionar datos relacionados con un sistema de psicología.

- Uso de bases de datos SQLite (psych_.db y psych_test.db) para almacenamiento persistente.

- Diseño de endpoints especializados para registro y consulta de información psicológica.

- Manejo de entidades personalizadas y posibles relaciones.

### ✅ Semana 7 - Proyecto Centro Estético

- Implementación de un proyecto temático orientado a un centro estético.

- Definición de entidades del negocio (clientes, citas, servicios, etc.).

- CRUD completo aplicado al caso real.

- Uso de validaciones y modelos para garantizar integridad de los datos.

### ✅ Semana 8 - Proyecto Lavandería

- Creación de una API para gestionar una lavandería como caso práctico final.

- Gestión de procesos básicos: clientes, pedidos, estados del servicio.

- Aplicación integral de lo aprendido: routers, servicios, modelos y validaciones.

- Consolidación de prácticas en proyectos completos listos para despliegue o mejora.