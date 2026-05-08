"""Schemas Pydantic — Conductores (Transportistas)"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ConductorBase(BaseModel):
    id_empleado: int = Field(..., description="ID del empleado")
    licencia_conducir: str = Field(..., min_length=5, max_length=50, description="Número de licencia")


class ConductorCreate(ConductorBase):
    pass


class ConductorUpdate(BaseModel):
    licencia_conducir: Optional[str] = Field(None, min_length=5, max_length=50)


class ConductorResponse(ConductorBase):
    model_config = ConfigDict(from_attributes=True)
    
    # Datos del empleado
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    estatus: Optional[str] = None


class ConductorListResponse(BaseModel):
    """Respuesta paginada para listado de conductores."""
    total: int
    skip: int
    limit: int
    data: list[ConductorResponse]
