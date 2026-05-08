"""Rutas del módulo de Autenticación"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.empleados import EmpleadoLogin, Token
from app.services.empleado_service import EmpleadoService

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/login", response_model=Token)
def login(credentials: EmpleadoLogin, db: Session = Depends(get_db)):
    """Login de usuario"""
    service = EmpleadoService(db)
    empleado = service.authenticate(credentials.email, credentials.password)
    
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token JWT
    access_token = service.create_access_token(empleado)
    
    # Convertir empleado a diccionario
    empleado_dict = {
        "id_empleado": empleado.id_empleado,
        "nombre": empleado.nombre,
        "apellido": empleado.apellido,
        "email": empleado.email,
        "cargo": empleado.cargo,
        "estatus": empleado.estatus
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "empleado": empleado_dict
    }


@router.post("/logout")
def logout():
    """Logout de usuario"""
    return {"message": "Logout exitoso"}


@router.get("/me")
def get_me():
    """Obtener información del usuario actual (por implementar con JWT)"""
    return {"message": "Endpoint para obtener usuario actual - Por implementar"}
