# 🚀 Backend ERP - Documentación

## Estructura del Proyecto

```
backend/
├── app/
│   ├── core/              # Configuración central
│   │   ├── config.py      # Configuración de Settings (Pydantic)
│   │   └── database.py    # Conexión y sesiones de BD
│   ├── api/               # Routers de módulos
│   │   ├── auth/          # Autenticación y JWT
│   │   ├── productos/     # Catálogo de productos
│   │   ├── inventario/    # Gestión de inventario
│   │   ├── compras/       # Gestión de compras
│   │   ├── ventas/        # Gestión de ventas
│   │   └── logistica/     # Gestión de envíos
│   ├── models/            # Modelos ORM (SQLAlchemy)
│   ├── schemas/           # Esquemas Pydantic (validación)
│   ├── repositories/      # Acceso a datos
│   ├── services/          # Lógica de negocio
│   ├── tasks/             # Tareas asincrónicas
│   └── utils/             # Utilidades
├── migrations/            # Migraciones Alembic
├── run.py                 # Punto de entrada
├── requirements.txt       # Dependencias
├── .env.example          # Variables de entorno (plantilla)
└── Dockerfile            # Containerización
```

## 📋 Requisitos

- Python 3.8+
- FastAPI
- SQLAlchemy
- Alembic (migraciones)
- Pydantic

## 🔧 Configuración

### 1. Crear archivo `.env`

Copia `.env.example` a `.env` y ajusta según tu entorno:

```bash
cp .env.example .env
```

Edita `.env` con tus valores:
- `DATABASE_URL`: Conexión a tu base de datos
- `SECRET_KEY`: Clave para JWT (genera una segura)
- `ENVIRONMENT`: `development` o `production`

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Crear tablas (primera ejecución)

```bash
# Opción 1: Usar Alembic (recomendado)
alembic upgrade head

# Opción 2: Script de generación
python split_models.py
```

## 🏃 Ejecutar la aplicación

```bash
# Desarrollo (con hot-reload)
python run.py

# O con uvicorn
uvicorn run:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: http://localhost:8000

## 📚 Documentación Interactiva

Una vez ejecutada la app:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## ✅ Health Check

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "database": "connected",
  "environment": "development"
}
```

## 🔑 Módulos Disponibles

| Módulo | Prefix | Tags | Estado |
|--------|--------|------|--------|
| Auth | `/auth` | Autenticación | 🚧 Por implementar |
| Productos | `/productos` | Productos | ✅ Implementado |
| Inventario | `/inventario` | Inventario | 🚧 Por implementar |
| Compras | `/compras` | Compras | 🚧 Por implementar |
| Ventas | `/ventas` | Ventas | 🚧 Por implementar |
| Logística | `/logistica` | Logística | 🚧 Por implementar |

## 🐳 Docker

```bash
# Construir imagen
docker build -f Dockerfile -t erp-api .

# Ejecutar contenedor
docker run -p 8000:8000 erp-api
```

## 📁 Estructura de un Módulo

Cada módulo debe tener:

```
modulo/
├── __init__.py
├── controllers.py       # Rutas (FastAPI router)
├── services.py          # Lógica de negocio
├── repositories.py      # Acceso a datos
└── schemas.py          # Validación (si es necesario)
```

### Ejemplo de Controllers

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/mi-modulo",
    tags=["Mi Módulo"],
)

@router.get("")
async def listar():
    return {"data": []}

@router.post("")
async def crear():
    return {"id": 1}
```

## 🔐 Variables de Entorno

```env
# Core
APP_NAME=ERP API
APP_VERSION=0.1.0
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=sqlite:///./test.db

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🚨 Troubleshooting

### Error: "No module named 'app.core.config'"
- Asegúrate que existe `backend/app/core/config.py`
- Verifica que tienes `.env` configurado

### Error de conexión a base de datos
- Verifica que `DATABASE_URL` en `.env` es correcta
- Ejecuta migraciones: `alembic upgrade head`

### Puerto 8000 ya está en uso
```bash
# Usar otro puerto
uvicorn run:app --port 8001
```

---

**Última actualización:** 20 de abril de 2026
