"""Schemas Pydantic — Reportes y Estadísticas"""
from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal


class VentaPeriodo(BaseModel):
    periodo: str
    total_ventas: int
    monto_total: Decimal
    promedio_por_venta: Decimal


class ResumenVentas(BaseModel):
    ventas_hoy: int
    ventas_semana: int
    ventas_mes: int
    monto_hoy: Decimal
    monto_semana: Decimal
    monto_mes: Decimal
    ventas_por_periodo: list[VentaPeriodo]


class ProductoMasVendido(BaseModel):
    id_producto: int
    nombre: str
    total_vendido: int
    monto_total: Decimal


class ResumenInventario(BaseModel):
    total_productos: int
    total_en_stock: int
    productos_bajo_stock: int
    valor_total_inventario: Decimal


class ResumenEmpleados(BaseModel):
    total: int
    activos: int
    inactivos: int
    por_cargo: list[dict]


class ResumenFinanciero(BaseModel):
    ventas_totales: Decimal
    compras_totales: Decimal
    ganancia_estimada: Decimal
    ventas_mes_actual: Decimal
    compras_mes_actual: Decimal


class ReporteDashboard(BaseModel):
    empleados: Optional[ResumenEmpleados] = None
    ventas: Optional[ResumenVentas] = None
    inventario: Optional[ResumenInventario] = None
    financiero: Optional[ResumenFinanciero] = None
    productos_mas_vendidos: Optional[list[ProductoMasVendido]] = None
