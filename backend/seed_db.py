"""Poblar base de datos con datos de prueba"""
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.empleados import Empleados
from app.models.clientes import Clientes
from app.models.proveedores import Proveedores
from app.models.marcas import Marcas
from app.models.categorias import Categorias
from app.models.unidades_medida import UnidadesMedida
from app.models.tipos_almacen import TiposAlmacen
from app.models.almacenes import Almacenes
from app.models.productos import Productos
from app.models.conductores import Conductores
from app.models.vehiculo import Vehiculo
from app.models.tipo_vehiculo import TipoVehiculo
from app.models.roles import Roles
from app.models.permisos import Permisos
from app.models.rol_permiso import RolPermiso
import datetime


def seed():
    db = SessionLocal()
    try:
        if db.query(Empleados).count() == 0:
            empleados = [
                Empleados(nombre="Admin", apellido="Sistema", email="admin@erp.com",
                          password_hash=get_password_hash("admin123"), cargo="Administrador",
                          telefono="555-0100", estatus="activo", fecha_registro=datetime.date.today()),
                Empleados(nombre="Juan", apellido="Perez", email="juan@test.com",
                          password_hash=get_password_hash("test123"), cargo="Vendedor",
                          telefono="555-0101", estatus="activo", fecha_registro=datetime.date.today()),
                Empleados(nombre="Maria", apellido="Lopez", email="maria@test.com",
                          password_hash=get_password_hash("test123"), cargo="Almacenista",
                          telefono="555-0102", estatus="activo", fecha_registro=datetime.date.today()),
                Empleados(nombre="Carlos", apellido="Garcia", email="carlos@test.com",
                          password_hash=get_password_hash("test123"), cargo="Contador",
                          telefono="555-0103", estatus="activo", fecha_registro=datetime.date.today()),
                Empleados(nombre="Ana", apellido="Martinez", email="ana@test.com",
                          password_hash=get_password_hash("test123"), cargo="Gerente",
                          telefono="555-0104", estatus="activo", fecha_registro=datetime.date.today()),
                Empleados(nombre="Pedro", apellido="Ramirez", email="pedro@test.com",
                          password_hash=get_password_hash("test123"), cargo="Transportista",
                          telefono="555-0105", estatus="activo", fecha_registro=datetime.date.today()),
            ]
            db.add_all(empleados); db.commit()
            for e in empleados: db.refresh(e)
            print(f"✓ {len(empleados)} empleados creados")
        else:
            empleados = db.query(Empleados).all()
            print(f"→ {len(empleados)} empleados ya existen")

        if db.query(Roles).count() == 0:
            roles = [
                Roles(nombre="Administrador", descripcion="Acceso total al sistema"),
                Roles(nombre="Vendedor", descripcion="Gestión de ventas y clientes"),
                Roles(nombre="Almacenista", descripcion="Gestión de inventario y almacenes"),
                Roles(nombre="Contador", descripcion="Gestión financiera y contable"),
                Roles(nombre="Gerente", descripcion="Supervisión general"),
                Roles(nombre="Transportista", descripcion="Gestión de envíos y rutas"),
            ]
            db.add_all(roles); db.commit()
            for r in roles: db.refresh(r)
            print(f"✓ {len(roles)} roles creados")
        else:
            roles = db.query(Roles).all()

        if db.query(Permisos).count() == 0:
            permisos = [
                Permisos(nombre="ver_empleados", descripcion="Ver listado de empleados"),
                Permisos(nombre="crear_empleados", descripcion="Crear nuevos empleados"),
                Permisos(nombre="editar_empleados", descripcion="Editar empleados"),
                Permisos(nombre="eliminar_empleados", descripcion="Eliminar empleados"),
                Permisos(nombre="ver_clientes", descripcion="Ver clientes"),
                Permisos(nombre="crear_clientes", descripcion="Crear clientes"),
                Permisos(nombre="ver_productos", descripcion="Ver productos"),
                Permisos(nombre="crear_productos", descripcion="Crear productos"),
                Permisos(nombre="ver_ventas", descripcion="Ver ventas"),
                Permisos(nombre="crear_ventas", descripcion="Crear ventas"),
                Permisos(nombre="ver_compras", descripcion="Ver compras"),
                Permisos(nombre="ver_inventario", descripcion="Ver inventario"),
                Permisos(nombre="ver_logistica", descripcion="Ver logística y envíos"),
                Permisos(nombre="ver_roles", descripcion="Ver roles y permisos"),
            ]
            db.add_all(permisos); db.commit()
            for p in permisos: db.refresh(p)
            print(f"✓ {len(permisos)} permisos creados")
        else:
            permisos = db.query(Permisos).all()

        if db.query(RolPermiso).count() == 0:
            pm = {p.nombre: p.id_permiso for p in db.query(Permisos).all()}
            rm = {r.nombre: r.id_rol for r in db.query(Roles).all()}
            asignaciones = {
                "Administrador": list(pm.values()),
                "Vendedor": [pm["ver_clientes"], pm["crear_clientes"], pm["ver_productos"], pm["ver_ventas"], pm["crear_ventas"]],
                "Almacenista": [pm["ver_productos"], pm["crear_productos"], pm["ver_inventario"]],
                "Contador": [pm["ver_compras"], pm["ver_ventas"]],
                "Gerente": [pm["ver_empleados"], pm["ver_clientes"], pm["ver_productos"], pm["ver_ventas"], pm["ver_compras"], pm["ver_inventario"]],
                "Transportista": [pm["ver_logistica"]],
            }
            for nombre_rol, pids in asignaciones.items():
                rid = rm.get(nombre_rol)
                if rid:
                    for pid in pids:
                        db.add(RolPermiso(id_rol=rid, id_permiso=pid))
            db.commit()
            print("✓ Permisos asignados a roles")

        if db.query(Clientes).count() == 0:
            clientes = [
                Clientes(nombre="Juan", apellido="Cliente", email="juan.cliente@email.com", telefono="555-1001", estatus="activo", fecha_registro=datetime.date.today()),
                Clientes(nombre="Maria", apellido="Luna", email="maria.luna@email.com", telefono="555-1002", estatus="activo", fecha_registro=datetime.date.today()),
                Clientes(nombre="Empresa", apellido="XYZ SA", email="contacto@xyzsa.com", telefono="555-1003", estatus="activo", fecha_registro=datetime.date.today()),
                Clientes(nombre="Pedro", apellido="Infante", email="pedro.i@email.com", telefono="555-1004", estatus="activo", fecha_registro=datetime.date.today()),
                Clientes(nombre="Laura", apellido="Diaz", email="laura.diaz@email.com", telefono="555-1005", estatus="activo", fecha_registro=datetime.date.today()),
            ]
            db.add_all(clientes); db.commit()
            for c in clientes: db.refresh(c)
            print(f"✓ {len(clientes)} clientes creados")
        else:
            print("→ Clientes ya existen")

        if db.query(Proveedores).count() == 0:
            proveedores = [
                Proveedores(nombre="Distribuidora Norte SA", direccion="Av. Reforma 100", email="ventas@distnorte.com", telefono="555-2001"),
                Proveedores(nombre="Importadora Global SA", direccion="Insurgentes 200", email="info@importglobal.com", telefono="555-2002"),
                Proveedores(nombre="Proveedor Local MX", direccion="Morelos 50", email="pedidos@proveedorlocal.com", telefono="555-2003"),
            ]
            db.add_all(proveedores); db.commit()
            for p in proveedores: db.refresh(p)
            print(f"✓ {len(proveedores)} proveedores creados")
        else:
            print("→ Proveedores ya existen")

        if db.query(Marcas).count() == 0:
            marcas = [
                Marcas(nombre="Nike", descripcion="Ropa y calzado deportivo"),
                Marcas(nombre="Samsung", descripcion="Electrónica y tecnología"),
                Marcas(nombre="Bic", descripcion="Artículos de escritorio"),
                Marcas(nombre="Genérica", descripcion="Productos genéricos"),
            ]
            db.add_all(marcas); db.commit()
            for m in marcas: db.refresh(m)
            print(f"✓ {len(marcas)} marcas creadas")
        else:
            print("→ Marcas ya existen")

        if db.query(Categorias).count() == 0:
            categorias = [
                Categorias(nombre="Electrónicos", descripcion="Productos electrónicos"),
                Categorias(nombre="Ropa", descripcion="Prendas de vestir"),
                Categorias(nombre="Papelería", descripcion="Artículos de oficina"),
                Categorias(nombre="Alimentos", descripcion="Productos alimenticios"),
                Categorias(nombre="Limpieza", descripcion="Productos de limpieza"),
            ]
            db.add_all(categorias); db.commit()
            for c in categorias: db.refresh(c)
            print(f"✓ {len(categorias)} categorías creadas")
        else:
            print("→ Categorías ya existen")

        if db.query(UnidadesMedida).count() == 0:
            unidades = [
                UnidadesMedida(nombre="Pieza", abreviatura="pz"),
                UnidadesMedida(nombre="Kilogramo", abreviatura="kg"),
                UnidadesMedida(nombre="Litro", abreviatura="l"),
                UnidadesMedida(nombre="Metro", abreviatura="m"),
                UnidadesMedida(nombre="Caja", abreviatura="cja"),
            ]
            db.add_all(unidades); db.commit()
            for u in unidades: db.refresh(u)
            print(f"✓ {len(unidades)} unidades de medida creadas")
        else:
            print("→ Unidades de medida ya existen")

        if db.query(TiposAlmacen).count() == 0:
            tipos = [
                TiposAlmacen(nombre="Principal", descripcion="Almacén central"),
                TiposAlmacen(nombre="Secundario", descripcion="Almacén de respaldo"),
                TiposAlmacen(nombre="Distribución", descripcion="Centro de distribución"),
            ]
            db.add_all(tipos); db.commit()
            for t in tipos: db.refresh(t)
            print(f"✓ {len(tipos)} tipos de almacén creados")
        else:
            print("→ Tipos de almacén ya existen")

        if db.query(Almacenes).count() == 0:
            tipo_alm = db.query(TiposAlmacen).first()
            admin = db.query(Empleados).filter(Empleados.cargo == "Administrador").first()
            admin_id = admin.id_empleado if admin else 1
            almacenes = [
                Almacenes(nombre="Almacén Central", ubicacion="Av. Principal 123", id_tipo_almacen=tipo_alm.id_tipo_almacen if tipo_alm else 1, id_empleado=admin_id),
                Almacenes(nombre="Almacén Norte", ubicacion="Calle Norte 456", id_tipo_almacen=tipo_alm.id_tipo_almacen if tipo_alm else 1, id_empleado=admin_id),
            ]
            db.add_all(almacenes); db.commit()
            for a in almacenes: db.refresh(a)
            print(f"✓ {len(almacenes)} almacenes creados")
        else:
            print("→ Almacenes ya existen")

        if db.query(TipoVehiculo).count() == 0:
            tipos_v = [
                TipoVehiculo(nombre="Camión", descripcion="Vehículo de carga pesada"),
                TipoVehiculo(nombre="Camioneta", descripcion="Vehículo de carga ligera"),
                TipoVehiculo(nombre="Moto", descripcion="Vehículo de entregas rápidas"),
            ]
            db.add_all(tipos_v); db.commit()
            for t in tipos_v: db.refresh(t)
            print(f"✓ {len(tipos_v)} tipos de vehículo creados")
        else:
            print("→ Tipos de vehículo ya existen")

        if db.query(Vehiculo).count() == 0:
            tipo_v = db.query(TipoVehiculo).first()
            vehiculos = [
                Vehiculo(placa="ABC-1234", marca="Toyota", modelo="Hilux", anio=2023, capacidad_carga=1500.00, id_tipo_vehiculo=tipo_v.id_tipo_vehiculo if tipo_v else 1),
                Vehiculo(placa="DEF-5678", marca="Nissan", modelo="NP300", anio=2022, capacidad_carga=1200.00, id_tipo_vehiculo=tipo_v.id_tipo_vehiculo if tipo_v else 1),
                Vehiculo(placa="GHI-9012", marca="Ford", modelo="Transit", anio=2024, capacidad_carga=800.00, id_tipo_vehiculo=tipo_v.id_tipo_vehiculo if tipo_v else 1),
            ]
            db.add_all(vehiculos); db.commit()
            for v in vehiculos: db.refresh(v)
            print(f"✓ {len(vehiculos)} vehículos creados")
        else:
            print("→ Vehículos ya existen")

        if db.query(Conductores).count() == 0:
            transportista = db.query(Empleados).filter(Empleados.cargo == "Transportista").first()
            if transportista:
                db.add(Conductores(id_empleado=transportista.id_empleado, licencia_conducir="LIC-ADM-001"))
                db.commit()
                print(f"✓ 1 conductor creado ({transportista.nombre})")
            else:
                print("⚠ No se encontró empleado con cargo Transportista")
        else:
            print("→ Conductores ya existen")

        if db.query(Productos).count() == 0:
            marca = db.query(Marcas).first()
            cat = db.query(Categorias).first()
            um = db.query(UnidadesMedida).first()
            if marca and cat and um:
                productos = [
                    Productos(nombre="Laptop básica", descripcion="Laptop para oficina", codigo="PROD-001", precio=15000.00, estatus="activo", id_marca=marca.id_marca, id_categoria=cat.id_categoria, id_unidad_medida=um.id_unidad_medida),
                    Productos(nombre='Monitor 24"', descripcion="Monitor LED 24 pulgadas", codigo="PROD-002", precio=4500.00, estatus="activo", id_marca=marca.id_marca, id_categoria=cat.id_categoria, id_unidad_medida=um.id_unidad_medida),
                    Productos(nombre="Teclado USB", descripcion="Teclado alámbrico USB", codigo="PROD-003", precio=350.00, estatus="activo", id_marca=marca.id_marca, id_categoria=cat.id_categoria, id_unidad_medida=um.id_unidad_medida),
                    Productos(nombre="Mouse óptico", descripcion="Mouse USB óptico", codigo="PROD-004", precio=180.00, estatus="activo", id_marca=marca.id_marca, id_categoria=cat.id_categoria, id_unidad_medida=um.id_unidad_medida),
                    Productos(nombre="Impresora multifuncional", descripcion="Impresora láser multifuncional", codigo="PROD-005", precio=3200.00, estatus="activo", id_marca=marca.id_marca, id_categoria=cat.id_categoria, id_unidad_medida=um.id_unidad_medida),
                ]
                db.add_all(productos); db.commit()
                print(f"✓ {len(productos)} productos creados")
            else:
                print("⚠ Faltan referencias para productos")
        else:
            print("→ Productos ya existen")

        print("\n" + "="*40)
        print("✅ BASE DE DATOS POBLADA EXITOSAMENTE")
        print("="*40)
        print("\nUsuarios disponibles:")
        print("  admin@erp.com / admin123  → Administrador")
        print("  juan@test.com / test123   → Vendedor")
        print("  maria@test.com / test123  → Almacenista")
        print("  carlos@test.com / test123 → Contador")
        print("  ana@test.com / test123    → Gerente")
        print("  pedro@test.com / test123  → Transportista")

    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Poblando base de datos...")
    seed()
