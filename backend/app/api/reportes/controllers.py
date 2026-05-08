"""Controllers — Reportes y Estadísticas"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role, require_auth
from app.services.reporte_service import ReporteService
from app.schemas.reportes import (
    ResumenVentas, ResumenInventario, ResumenEmpleados,
    ResumenFinanciero, ProductoMasVendido, ReporteDashboard,
)

router = APIRouter(prefix="/reportes", tags=["Reportes"],
                   dependencies=[Depends(require_role(["Administrador", "Gerente", "Vendedor", "Almacenista", "Contador"]))])


@router.get("/dashboard", response_model=ReporteDashboard,
            summary="Dashboard completo según el rol del usuario")
def dashboard(
    db: Session = Depends(get_db),
    empleado: dict = Depends(require_auth),
):
    return ReporteService(db).dashboard_completo(empleado["cargo"])


@router.get("/ventas", response_model=ResumenVentas,
            summary="Resumen de ventas (hoy, semana, mes)")
def resumen_ventas(db: Session = Depends(get_db)):
    return ReporteService(db).resumen_ventas()


@router.get("/inventario", response_model=ResumenInventario,
            summary="Resumen del inventario")
def resumen_inventario(db: Session = Depends(get_db)):
    return ReporteService(db).resumen_inventario()


@router.get("/empleados", response_model=ResumenEmpleados,
            summary="Estadísticas de empleados")
def resumen_empleados(db: Session = Depends(get_db)):
    return ReporteService(db).resumen_empleados()


@router.get("/financiero", response_model=ResumenFinanciero,
            summary="Resumen financiero (ventas vs compras)")
def resumen_financiero(db: Session = Depends(get_db)):
    return ReporteService(db).resumen_financiero()


@router.get("/productos-mas-vendidos", response_model=list[ProductoMasVendido],
            summary="Top productos más vendidos")
def productos_mas_vendidos(
    limite: int = 10,
    db: Session = Depends(get_db),
):
    return ReporteService(db).productos_mas_vendidos(limite)
