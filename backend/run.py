# backend/run.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import engine, get_db, Base
from app.core.config import settings
from app.api.auth.controllers import router as auth_router
from app.api.inventario.controllers import router as inventario_router
from app.api.compras.controllers import router as compras_router
from app.api.ventas.controllers import router as ventas_router
from app.api.logistica.controllers import router as logistica_router
from app.api.productos.controllers import router as productos_router
from app.api.roles.controllers import router as roles_router
from app.api.empleados.controllers import router as empleados_router
from app.api.clientes.controllers import router as clientes_router
from app.api.proveedores.controllers import router as proveedores_router

app = FastAPI(
    title=settings.app_name,
    description="Sistema ERP — API REST",
    version=settings.app_version,
    openapi_tags=[
        {"name": "General"},
        {"name": "Autenticación"},
        {"name": "Roles & Permisos"},
        {"name": "Empleados"},
        {"name": "Clientes"},
        {"name": "Proveedores"},
        {"name": "Productos"},
        {"name": "Inventario"},
        {"name": "Compras"},
        {"name": "Ventas"},
        {"name": "Logística"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(empleados_router)
app.include_router(clientes_router)
app.include_router(proveedores_router)
app.include_router(productos_router)
app.include_router(inventario_router)
app.include_router(compras_router)
app.include_router(ventas_router)
app.include_router(logistica_router)


@app.get("/", tags=["General"])
def root():
    return {
        "message": "ERP API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["General"])
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "environment": settings.environment}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info",
    )