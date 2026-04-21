"""Rutas del módulo de Autenticación"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/login")
async def login():
    """Login de usuario (por implementar)"""
    return {"message": "Login endpoint - Por implementar"}


@router.post("/logout")
async def logout():
    """Logout de usuario (por implementar)"""
    return {"message": "Logout endpoint - Por implementar"}


@router.post("/register")
async def register():
    """Registro de usuario (por implementar)"""
    return {"message": "Register endpoint - Por implementar"}
