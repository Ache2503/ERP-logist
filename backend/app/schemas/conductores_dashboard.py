"""Schemas — Conductores Dashboard"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class ConductorPerfilUpdate(BaseModel):
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[str] = None


class ConductorPerfilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_empleado: int
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    cargo: str
    estatus: str
    licencia_conducir: Optional[str] = None


class ConductorStats(BaseModel):
    total_asignados: int
    en_ruta: int
    entregados: int
    fallidos: int
    pendientes: int
    total_incidentes: int
    calificacion_promedio: float
    total_resenas: int


class EnvioDetalleProducto(BaseModel):
    id_producto: int
    nombre: str
    cantidad: int
    precio_unitario: Decimal


class EnvioClienteInfo(BaseModel):
    id_cliente: int
    nombre: str
    apellido: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None


class EnvioDetalleCompleto(BaseModel):
    id_envio: int
    fecha_envio: date
    estatus: str
    id_pedido_cliente: int
    pedido_fecha: Optional[date] = None
    pedido_total: Optional[Decimal] = None
    pedido_estatus: Optional[str] = None
    vehiculo_placa: Optional[str] = None
    vehiculo_marca: Optional[str] = None
    vehiculo_modelo: Optional[str] = None
    cliente: Optional[EnvioClienteInfo] = None
    productos: list[EnvioDetalleProducto] = []
    seguimiento: list[dict] = []


class IncidenteCreate(BaseModel):
    id_envio: int
    tipo: str = Field(..., description="Tipo: accidente, retraso, averia, otro")
    descripcion: str
    evidencia: Optional[str] = None


class IncidenteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_incidente: int
    id_envio: int
    id_empleado: int
    tipo: str
    descripcion: str
    fecha_reporte: datetime
    estatus: str
    evidencia: Optional[str] = None


class ResenaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_resena: int
    calificacion: int
    comentario: Optional[str] = None
    fecha_resena: datetime
    cliente_nombre: Optional[str] = None


class IncidenteListResponse(BaseModel):
    total: int
    data: list[IncidenteResponse]
