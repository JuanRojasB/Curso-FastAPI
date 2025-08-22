# 🌐 Proyecto FastAPI - Bootcamp

👨‍💻 Autor: Juan David Rojas Burbano 
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
