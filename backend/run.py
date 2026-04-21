# backend/run.py
"""
Punto de entrada principal de la aplicación FastAPI ERP
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import engine, get_db, Base
from app.core.config import settings

# Importar routers de los módulos
from app.api.auth.controllers import router as auth_router
from app.api.inventario.controllers import router as inventario_router
from app.api.compras.controllers import router as compras_router
from app.api.ventas.controllers import router as ventas_router
from app.api.logistica.controllers import router as logistica_router
from app.api.productos.controllers import router as productos_router

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="Sistema de gestión empresarial (ERP) - Módulos: Inventario, Ventas, Compras, Logística, RRHH",
    version=settings.app_version,
    openapi_tags=[
        {"name": "General", "description": "Endpoints generales de la aplicación"},
        {"name": "Autenticación", "description": "Login y gestión de tokens JWT"},
        {"name": "Productos", "description": "CRUD de productos del catálogo"},
        {"name": "Inventario", "description": "Gestión de inventario y almacenes"},
        {"name": "Compras", "description": "Gestión de compras a proveedores"},
        {"name": "Ventas", "description": "Gestión de ventas a clientes"},
        {"name": "Logística", "description": "Gestión de envíos y transporte"},
    ],
)

# Configurar CORS con settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers en orden lógico
app.include_router(auth_router)
app.include_router(productos_router)
app.include_router(inventario_router)
app.include_router(compras_router)
app.include_router(ventas_router)
app.include_router(logistica_router)


# Endpoint raíz informativo
@app.get("/", tags=["General"])
def root():
    """Endpoint raíz con información general de la API"""
    return {
        "message": "Bienvenido a ERP API",
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs",
        "health": "/health",
    }


# Health check que valida conexión a BD
@app.get("/health", tags=["General"])
def health_check(db: Session = Depends(get_db)):
    """Verifica el estado de la API y la conexión a base de datos"""
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
            "environment": settings.environment
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning",
    )