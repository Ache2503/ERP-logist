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


class ConductorEnvioResponse(BaseModel):
    """Envío asignado a un conductor con datos del pedido"""
    model_config = ConfigDict(from_attributes=True)
    id_asignacion: int
    id_envio: int
    id_pedido_cliente: int
    id_cliente: Optional[int] = None
    cliente_nombre: Optional[str] = None
    total_pedido: Optional[float] = None
    estatus_envio: Optional[str] = None
    estatus_pedido: Optional[str] = None
    fecha_asignacion: Optional[str] = None
    requiere_envio: Optional[int] = None


class ConductorEnvioListResponse(BaseModel):
    """Respuesta paginada de envíos asignados a un conductor"""
    total: int
    data: list[ConductorEnvioResponse]
