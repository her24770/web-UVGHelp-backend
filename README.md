# UVGHelp Backend

API REST para el sistema de información universitaria UVGHelp — Universidad del Valle de Guatemala.

## Stack

- Python 3.11 + FastAPI
- PostgreSQL 15
- SQLAlchemy 2 + Alembic
- Docker + Docker Compose

## Correr el proyecto

### Requisitos
- Docker
- Docker Compose

### Pasos

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd uvghelp-backend

# 2. Copiar variables de entorno
cp .env.example .env

# 3. Levantar todo
docker compose up --build
```

La API estará disponible en:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Challenges implementados

- Spec OpenAPI/Swagger
- Códigos HTTP correctos
- Validación server-side
- Paginación (`?page=`, `?limit=`)
- Búsqueda (`?q=`)
- Ordenamiento (`?sort=`, `?order=`)
- Export CSV
- Export Excel (XLSX)
- Upload de imágenes (máx 1MB)

## Reflexión

<!-- Agregar reflexión antes de entregar -->
