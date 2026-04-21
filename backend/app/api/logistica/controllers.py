"""Rutas del módulo de Logística"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/logistica",
    tags=["Logística"],
    responses={404: {"description": "No encontrado"}},
)


@router.get("")
async def listar_envios():
    """Lista todos los envíos (por implementar)"""
    return {"message": "Listar envíos - Por implementar"}


@router.post("")
async def crear_envio():
    """Crea un nuevo envío (por implementar)"""
    return {"message": "Crear envío - Por implementar"}


@router.get("/{id}")
async def obtener_envio(id: int):
    """Obtiene un envío específico (por implementar)"""
    return {"message": f"Obtener envío {id} - Por implementar"}
