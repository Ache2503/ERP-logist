"""Rutas del módulo de Inventario"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario"],
    responses={404: {"description": "No encontrado"}},
)


@router.get("")
async def listar_inventario():
    """Lista el inventario (por implementar)"""
    return {"message": "Listar inventario - Por implementar"}


@router.get("/{id}")
async def obtener_inventario(id: int):
    """Obtiene detalles del inventario (por implementar)"""
    return {"message": f"Obtener inventario {id} - Por implementar"}
