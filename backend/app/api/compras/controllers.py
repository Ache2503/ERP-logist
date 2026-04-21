"""Rutas del módulo de Compras"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/compras",
    tags=["Compras"],
    responses={404: {"description": "No encontrado"}},
)


@router.get("")
async def listar_compras():
    """Lista todas las compras (por implementar)"""
    return {"message": "Listar compras - Por implementar"}


@router.post("")
async def crear_compra():
    """Crea una nueva compra (por implementar)"""
    return {"message": "Crear compra - Por implementar"}


@router.get("/{id}")
async def obtener_compra(id: int):
    """Obtiene una compra específica (por implementar)"""
    return {"message": f"Obtener compra {id} - Por implementar"}
