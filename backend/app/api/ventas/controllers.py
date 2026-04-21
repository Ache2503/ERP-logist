"""Rutas del módulo de Ventas"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"],
    responses={404: {"description": "No encontrado"}},
)


@router.get("")
async def listar_ventas():
    """Lista todas las ventas (por implementar)"""
    return {"message": "Listar ventas - Por implementar"}


@router.post("")
async def crear_venta():
    """Crea una nueva venta (por implementar)"""
    return {"message": "Crear venta - Por implementar"}


@router.get("/{id}")
async def obtener_venta(id: int):
    """Obtiene una venta específica (por implementar)"""
    return {"message": f"Obtener venta {id} - Por implementar"}
