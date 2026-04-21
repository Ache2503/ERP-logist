from typing import Optional
import datetime
import decimal

from sqlalchemy import CheckConstraint, DECIMAL, Date, DateTime, ForeignKeyConstraint, Index, Integer, String, Text, Time, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Backups(Base):
    __tablename__ = 'backups'

    id_backup: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_backup: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    ruta_archivo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)


class CategoriaPadre(Base):
    __tablename__ = 'categoria_padre'

    id_categoria_padre: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(200))

    categorias: Mapped[list['Categorias']] = relationship('Categorias', back_populates='categoria_padre')


class Clientes(Base):
    __tablename__ = 'clientes'
    __table_args__ = (
        Index('email', 'email', unique=True),
        Index('rfc', 'rfc', unique=True)
    )

    id_cliente: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))
    fecha_registro: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    apellido: Mapped[Optional[str]] = mapped_column(String(100))
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    rfc: Mapped[Optional[str]] = mapped_column(String(13))

    pedidos_clientes: Mapped[list['PedidosClientes']] = relationship('PedidosClientes', back_populates='clientes')


class Configuracion(Base):
    __tablename__ = 'configuracion'
    __table_args__ = (
        Index('clave', 'clave', unique=True),
    )

    id_configuracion: Mapped[int] = mapped_column(Integer, primary_key=True)
    clave: Mapped[str] = mapped_column(String(50), nullable=False)
    valor: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)


class Empleados(Base):
    __tablename__ = 'empleados'
    __table_args__ = (
        Index('email', 'email', unique=True),
        Index('numero_seguridad_social', 'numero_seguridad_social', unique=True),
        Index('rfc', 'rfc', unique=True)
    )

    id_empleado: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))
    fecha_registro: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    rfc: Mapped[Optional[str]] = mapped_column(String(13))
    numero_seguridad_social: Mapped[Optional[str]] = mapped_column(String(20))
    cargo: Mapped[Optional[str]] = mapped_column(String(50))

    almacenes: Mapped[list['Almacenes']] = relationship('Almacenes', back_populates='empleados')
    auditoria: Mapped[list['Auditoria']] = relationship('Auditoria', back_populates='empleados')
    empleado_rol: Mapped[list['EmpleadoRol']] = relationship('EmpleadoRol', back_populates='empleados')
    movimiento: Mapped[list['Movimiento']] = relationship('Movimiento', back_populates='empleados')
    compras: Mapped[list['Compras']] = relationship('Compras', back_populates='empleados')
    pedidos_clientes: Mapped[list['PedidosClientes']] = relationship('PedidosClientes', back_populates='empleados')
    pedidos_proveedores: Mapped[list['PedidosProveedores']] = relationship('PedidosProveedores', back_populates='empleados')
    traslados_internos: Mapped[list['TrasladosInternos']] = relationship('TrasladosInternos', back_populates='empleados')
    envios: Mapped[list['Envios']] = relationship('Envios', back_populates='empleados')


class Marcas(Base):
    __tablename__ = 'marcas'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id_marca: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    productos: Mapped[list['Productos']] = relationship('Productos', back_populates='marcas')


class Permisos(Base):
    __tablename__ = 'permisos'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id_permiso: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    rol_permiso: Mapped[list['RolPermiso']] = relationship('RolPermiso', back_populates='permisos')


class Proveedores(Base):
    __tablename__ = 'proveedores'

    id_proveedor: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))

    proveedor_contacto: Mapped[list['ProveedorContacto']] = relationship('ProveedorContacto', back_populates='proveedores')
    compras: Mapped[list['Compras']] = relationship('Compras', back_populates='proveedores')
    pedidos_proveedores: Mapped[list['PedidosProveedores']] = relationship('PedidosProveedores', back_populates='proveedores')


class Restauraciones(Base):
    __tablename__ = 'restauraciones'

    id_restauracion: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_restauracion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    ruta_archivo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    empleado_rol: Mapped[list['EmpleadoRol']] = relationship('EmpleadoRol', back_populates='roles')
    rol_permiso: Mapped[list['RolPermiso']] = relationship('RolPermiso', back_populates='roles')


class Ruta(Base):
    __tablename__ = 'ruta'

    id_ruta: Mapped[int] = mapped_column(Integer, primary_key=True)
    origen: Mapped[str] = mapped_column(String(100), nullable=False)
    destino: Mapped[str] = mapped_column(String(100), nullable=False)
    distancia: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    tiempo_estimado: Mapped[Optional[datetime.time]] = mapped_column(Time)

    ruta_envio: Mapped[list['RutaEnvio']] = relationship('RutaEnvio', back_populates='ruta')


class TipoVehiculo(Base):
    __tablename__ = 'tipo_vehiculo'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id_tipo_vehiculo: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    vehiculo: Mapped[list['Vehiculo']] = relationship('Vehiculo', back_populates='tipo_vehiculo')


class TiposAlmacen(Base):
    __tablename__ = 'tipos_almacen'
    __table_args__ = (
        Index('nombre_tipo', 'nombre_tipo', unique=True),
    )

    id_tipo_almacen: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    almacenes: Mapped[list['Almacenes']] = relationship('Almacenes', back_populates='tipos_almacen')


class UnidadesMedida(Base):
    __tablename__ = 'unidades_medida'
    __table_args__ = (
        Index('abreviatura', 'abreviatura', unique=True),
    )

    id_unidad_medida: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    abreviatura: Mapped[str] = mapped_column(String(10), nullable=False)

    productos: Mapped[list['Productos']] = relationship('Productos', back_populates='unidades_medida')


class Almacenes(Base):
    __tablename__ = 'almacenes'
    __table_args__ = (
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='almacenes_ibfk_1'),
        ForeignKeyConstraint(['id_tipo_almacen'], ['tipos_almacen.id_tipo_almacen'], name='almacenes_ibfk_2'),
        Index('idx_almacen_empleado', 'id_empleado'),
        Index('idx_almacen_tipo', 'id_tipo_almacen')
    )

    id_almacen: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_tipo_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    ubicacion: Mapped[Optional[str]] = mapped_column(String(200))

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='almacenes')
    tipos_almacen: Mapped['TiposAlmacen'] = relationship('TiposAlmacen', back_populates='almacenes')
    compras: Mapped[list['Compras']] = relationship('Compras', back_populates='almacenes')
    pedidos_clientes: Mapped[list['PedidosClientes']] = relationship('PedidosClientes', back_populates='almacenes')
    pedidos_proveedores: Mapped[list['PedidosProveedores']] = relationship('PedidosProveedores', back_populates='almacenes')
    traslados_internos_id_almacen_destino: Mapped[list['TrasladosInternos']] = relationship('TrasladosInternos', foreign_keys='[TrasladosInternos.id_almacen_destino]', back_populates='almacenes')
    traslados_internos_id_almacen_origen: Mapped[list['TrasladosInternos']] = relationship('TrasladosInternos', foreign_keys='[TrasladosInternos.id_almacen_origen]', back_populates='almacenes_')
    movimiento_detalle: Mapped[list['MovimientoDetalle']] = relationship('MovimientoDetalle', back_populates='almacenes')
    productos_almacen: Mapped[list['ProductosAlmacen']] = relationship('ProductosAlmacen', back_populates='almacenes')


class Auditoria(Base):
    __tablename__ = 'auditoria'
    __table_args__ = (
        ForeignKeyConstraint(['id_usuario'], ['empleados.id_empleado'], name='auditoria_ibfk_1'),
        Index('idx_auditoria_fecha', 'fecha'),
        Index('idx_auditoria_usuario', 'id_usuario')
    )

    id_auditoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    accion: Mapped[str] = mapped_column(String(50), nullable=False)
    tabla: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    detalles: Mapped[Optional[str]] = mapped_column(Text)

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='auditoria')


class Categorias(Base):
    __tablename__ = 'categorias'
    __table_args__ = (
        ForeignKeyConstraint(['id_categoria_padre'], ['categoria_padre.id_categoria_padre'], name='categorias_ibfk_1'),
        Index('idx_categoria_padre', 'id_categoria_padre')
    )

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    id_categoria_padre: Mapped[Optional[int]] = mapped_column(Integer)

    categoria_padre: Mapped[Optional['CategoriaPadre']] = relationship('CategoriaPadre', back_populates='categorias')
    productos: Mapped[list['Productos']] = relationship('Productos', back_populates='categorias')


class Conductores(Empleados):
    __tablename__ = 'conductores'
    __table_args__ = (
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], ondelete='CASCADE', name='conductores_ibfk_1'),
        Index('licencia_conducir', 'licencia_conducir', unique=True)
    )

    id_empleado: Mapped[int] = mapped_column(Integer, primary_key=True)
    licencia_conducir: Mapped[str] = mapped_column(String(50), nullable=False)

    guia_remision: Mapped[list['GuiaRemision']] = relationship('GuiaRemision', back_populates='conductores')
    asignacion_transporte: Mapped[list['AsignacionTransporte']] = relationship('AsignacionTransporte', back_populates='conductores')


class EmpleadoRol(Base):
    __tablename__ = 'empleado_rol'
    __table_args__ = (
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], ondelete='CASCADE', name='empleado_rol_ibfk_1'),
        ForeignKeyConstraint(['id_rol'], ['roles.id_rol'], ondelete='CASCADE', name='empleado_rol_ibfk_2'),
        Index('id_rol', 'id_rol'),
        Index('uk_empleado_rol', 'id_empleado', 'id_rol', unique=True)
    )

    id_empleado_rol: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_rol: Mapped[int] = mapped_column(Integer, nullable=False)

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='empleado_rol')
    roles: Mapped['Roles'] = relationship('Roles', back_populates='empleado_rol')


class Movimiento(Base):
    __tablename__ = 'movimiento'
    __table_args__ = (
        ForeignKeyConstraint(['id_usuario'], ['empleados.id_empleado'], name='movimiento_ibfk_1'),
        Index('idx_movimiento_fecha', 'fecha'),
        Index('idx_movimiento_usuario', 'id_usuario')
    )

    id_movimiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    tipo_movimiento: Mapped[str] = mapped_column(String(20), nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(Text)

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='movimiento')
    compra_detalle: Mapped[list['CompraDetalle']] = relationship('CompraDetalle', back_populates='movimiento')
    movimiento_detalle: Mapped[list['MovimientoDetalle']] = relationship('MovimientoDetalle', back_populates='movimiento')


class ProveedorContacto(Base):
    __tablename__ = 'proveedor_contacto'
    __table_args__ = (
        ForeignKeyConstraint(['id_proveedor'], ['proveedores.id_proveedor'], name='proveedor_contacto_ibfk_1'),
        Index('idx_contacto_proveedor', 'id_proveedor')
    )

    id_contacto: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_proveedor: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(100))

    proveedores: Mapped['Proveedores'] = relationship('Proveedores', back_populates='proveedor_contacto')


class RolPermiso(Base):
    __tablename__ = 'rol_permiso'
    __table_args__ = (
        ForeignKeyConstraint(['id_permiso'], ['permisos.id_permiso'], ondelete='CASCADE', name='rol_permiso_ibfk_2'),
        ForeignKeyConstraint(['id_rol'], ['roles.id_rol'], ondelete='CASCADE', name='rol_permiso_ibfk_1'),
        Index('id_permiso', 'id_permiso'),
        Index('uk_rol_permiso', 'id_rol', 'id_permiso', unique=True)
    )

    id_rol_permiso: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_rol: Mapped[int] = mapped_column(Integer, nullable=False)
    id_permiso: Mapped[int] = mapped_column(Integer, nullable=False)

    permisos: Mapped['Permisos'] = relationship('Permisos', back_populates='rol_permiso')
    roles: Mapped['Roles'] = relationship('Roles', back_populates='rol_permiso')


class Vehiculo(Base):
    __tablename__ = 'vehiculo'
    __table_args__ = (
        ForeignKeyConstraint(['id_tipo_vehiculo'], ['tipo_vehiculo.id_tipo_vehiculo'], name='vehiculo_ibfk_1'),
        Index('idx_vehiculo_tipo', 'id_tipo_vehiculo'),
        Index('numero_serie', 'numero_serie', unique=True),
        Index('placa', 'placa', unique=True)
    )

    id_vehiculo: Mapped[int] = mapped_column(Integer, primary_key=True)
    placa: Mapped[str] = mapped_column(String(20), nullable=False)
    marca: Mapped[str] = mapped_column(String(50), nullable=False)
    id_tipo_vehiculo: Mapped[int] = mapped_column(Integer, nullable=False)
    modelo: Mapped[Optional[str]] = mapped_column(String(50))
    anio: Mapped[Optional[int]] = mapped_column(Integer)
    numero_serie: Mapped[Optional[str]] = mapped_column(String(50))
    capacidad_carga: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))

    tipo_vehiculo: Mapped['TipoVehiculo'] = relationship('TipoVehiculo', back_populates='vehiculo')
    mantenimiento_vehiculo: Mapped[list['MantenimientoVehiculo']] = relationship('MantenimientoVehiculo', back_populates='vehiculo')
    envios: Mapped[list['Envios']] = relationship('Envios', back_populates='vehiculo')
    guia_remision: Mapped[list['GuiaRemision']] = relationship('GuiaRemision', back_populates='vehiculo')


class Compras(Base):
    __tablename__ = 'compras'
    __table_args__ = (
        CheckConstraint('(`subtotal` >= 0)', name='compras_chk_1'),
        ForeignKeyConstraint(['id_almacen'], ['almacenes.id_almacen'], name='compras_ibfk_2'),
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='compras_ibfk_3'),
        ForeignKeyConstraint(['id_proveedor'], ['proveedores.id_proveedor'], name='compras_ibfk_1'),
        Index('idx_compra_almacen', 'id_almacen'),
        Index('idx_compra_empleado', 'id_empleado'),
        Index('idx_compra_proveedor', 'id_proveedor')
    )

    id_compra: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_compra: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_proveedor: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pendiente'"))
    tipo_comprobante: Mapped[Optional[str]] = mapped_column(String(50))
    serie: Mapped[Optional[str]] = mapped_column(String(20))
    numero: Mapped[Optional[str]] = mapped_column(String(20))

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', back_populates='compras')
    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='compras')
    proveedores: Mapped['Proveedores'] = relationship('Proveedores', back_populates='compras')
    compra_detalle: Mapped[list['CompraDetalle']] = relationship('CompraDetalle', back_populates='compras')


class MantenimientoVehiculo(Base):
    __tablename__ = 'mantenimiento_vehiculo'
    __table_args__ = (
        ForeignKeyConstraint(['id_vehiculo'], ['vehiculo.id_vehiculo'], name='mantenimiento_vehiculo_ibfk_1'),
        Index('id_vehiculo', 'id_vehiculo')
    )

    id_mantenimiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_vehiculo: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_mantenimiento: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    costo: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))

    vehiculo: Mapped['Vehiculo'] = relationship('Vehiculo', back_populates='mantenimiento_vehiculo')


class PedidosClientes(Base):
    __tablename__ = 'pedidos_clientes'
    __table_args__ = (
        CheckConstraint('(`subtotal` >= 0)', name='pedidos_clientes_chk_1'),
        CheckConstraint('(`total` >= 0)', name='pedidos_clientes_chk_2'),
        ForeignKeyConstraint(['id_almacen'], ['almacenes.id_almacen'], name='pedidos_clientes_ibfk_3'),
        ForeignKeyConstraint(['id_cliente'], ['clientes.id_cliente'], name='pedidos_clientes_ibfk_1'),
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='pedidos_clientes_ibfk_2'),
        Index('idx_pc_almacen', 'id_almacen'),
        Index('idx_pc_cliente', 'id_cliente'),
        Index('idx_pc_empleado', 'id_empleado')
    )

    id_pedido_cliente: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    impuesto: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False, server_default=text("'0.00'"))
    total: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pendiente'"))
    requiere_envio: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', back_populates='pedidos_clientes')
    clientes: Mapped['Clientes'] = relationship('Clientes', back_populates='pedidos_clientes')
    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='pedidos_clientes')
    devoluciones_clientes: Mapped[list['DevolucionesClientes']] = relationship('DevolucionesClientes', back_populates='pedidos_clientes')
    envios: Mapped[list['Envios']] = relationship('Envios', back_populates='pedidos_clientes')
    guia_remision: Mapped[list['GuiaRemision']] = relationship('GuiaRemision', back_populates='pedidos_clientes')
    pedido_cliente_detalle: Mapped[list['PedidoClienteDetalle']] = relationship('PedidoClienteDetalle', back_populates='pedidos_clientes')


class PedidosProveedores(Base):
    __tablename__ = 'pedidos_proveedores'
    __table_args__ = (
        ForeignKeyConstraint(['id_almacen'], ['almacenes.id_almacen'], name='pedidos_proveedores_ibfk_3'),
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='pedidos_proveedores_ibfk_2'),
        ForeignKeyConstraint(['id_proveedor'], ['proveedores.id_proveedor'], name='pedidos_proveedores_ibfk_1'),
        Index('id_almacen', 'id_almacen'),
        Index('idx_pp_empleado', 'id_empleado'),
        Index('idx_pp_proveedor', 'id_proveedor')
    )

    id_pedido_proveedor: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_proveedor: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    impuesto: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False, server_default=text("'0.00'"))
    total: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pendiente'"))

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', back_populates='pedidos_proveedores')
    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='pedidos_proveedores')
    proveedores: Mapped['Proveedores'] = relationship('Proveedores', back_populates='pedidos_proveedores')
    devoluciones_proveedores: Mapped[list['DevolucionesProveedores']] = relationship('DevolucionesProveedores', back_populates='pedidos_proveedores')
    pedido_proveedor_detalle: Mapped[list['PedidoProveedorDetalle']] = relationship('PedidoProveedorDetalle', back_populates='pedidos_proveedores')


class Productos(Base):
    __tablename__ = 'productos'
    __table_args__ = (
        CheckConstraint('(`precio` >= 0)', name='productos_chk_1'),
        ForeignKeyConstraint(['id_categoria'], ['categorias.id_categoria'], name='productos_ibfk_1'),
        ForeignKeyConstraint(['id_marca'], ['marcas.id_marca'], name='productos_ibfk_2'),
        ForeignKeyConstraint(['id_unidad_medida'], ['unidades_medida.id_unidad_medida'], name='productos_ibfk_3'),
        Index('codigo', 'codigo', unique=True),
        Index('idx_producto_categoria', 'id_categoria'),
        Index('idx_producto_marca', 'id_marca'),
        Index('idx_producto_um', 'id_unidad_medida')
    )

    id_producto: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    id_categoria: Mapped[int] = mapped_column(Integer, nullable=False)
    id_marca: Mapped[int] = mapped_column(Integer, nullable=False)
    id_unidad_medida: Mapped[int] = mapped_column(Integer, nullable=False)
    precio: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    categorias: Mapped['Categorias'] = relationship('Categorias', back_populates='productos')
    marcas: Mapped['Marcas'] = relationship('Marcas', back_populates='productos')
    unidades_medida: Mapped['UnidadesMedida'] = relationship('UnidadesMedida', back_populates='productos')
    compra_detalle: Mapped[list['CompraDetalle']] = relationship('CompraDetalle', back_populates='productos')
    movimiento_detalle: Mapped[list['MovimientoDetalle']] = relationship('MovimientoDetalle', back_populates='productos')
    pedido_cliente_detalle: Mapped[list['PedidoClienteDetalle']] = relationship('PedidoClienteDetalle', back_populates='productos')
    pedido_proveedor_detalle: Mapped[list['PedidoProveedorDetalle']] = relationship('PedidoProveedorDetalle', back_populates='productos')
    productos_almacen: Mapped[list['ProductosAlmacen']] = relationship('ProductosAlmacen', back_populates='productos')
    traslado_interno_detalle: Mapped[list['TrasladoInternoDetalle']] = relationship('TrasladoInternoDetalle', back_populates='productos')
    devolucion_cliente_detalle: Mapped[list['DevolucionClienteDetalle']] = relationship('DevolucionClienteDetalle', back_populates='productos')
    devolucion_proveedor_detalle: Mapped[list['DevolucionProveedorDetalle']] = relationship('DevolucionProveedorDetalle', back_populates='productos')
    envio_detalle: Mapped[list['EnvioDetalle']] = relationship('EnvioDetalle', back_populates='productos')
    guia_remision_detalle: Mapped[list['GuiaRemisionDetalle']] = relationship('GuiaRemisionDetalle', back_populates='productos')


class TrasladosInternos(Base):
    __tablename__ = 'traslados_internos'
    __table_args__ = (
        CheckConstraint('(`id_almacen_origen` <> `id_almacen_destino`)', name='traslados_internos_chk_1'),
        ForeignKeyConstraint(['id_almacen_destino'], ['almacenes.id_almacen'], name='traslados_internos_ibfk_2'),
        ForeignKeyConstraint(['id_almacen_origen'], ['almacenes.id_almacen'], name='traslados_internos_ibfk_1'),
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='traslados_internos_ibfk_3'),
        Index('id_almacen_destino', 'id_almacen_destino'),
        Index('id_almacen_origen', 'id_almacen_origen'),
        Index('id_empleado', 'id_empleado')
    )

    id_traslado: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_traslado: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_almacen_origen: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen_destino: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False)

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', foreign_keys=[id_almacen_destino], back_populates='traslados_internos_id_almacen_destino')
    almacenes_: Mapped['Almacenes'] = relationship('Almacenes', foreign_keys=[id_almacen_origen], back_populates='traslados_internos_id_almacen_origen')
    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='traslados_internos')
    traslado_interno_detalle: Mapped[list['TrasladoInternoDetalle']] = relationship('TrasladoInternoDetalle', back_populates='traslados_internos')


class CompraDetalle(Base):
    __tablename__ = 'compra_detalle'
    __table_args__ = (
        CheckConstraint('(`cantidad` > 0)', name='compra_detalle_chk_1'),
        CheckConstraint('(`precio_unitario` >= 0)', name='compra_detalle_chk_2'),
        CheckConstraint('(`subtotal` >= 0)', name='compra_detalle_chk_3'),
        ForeignKeyConstraint(['id_compra'], ['compras.id_compra'], ondelete='CASCADE', name='compra_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_movimiento'], ['movimiento.id_movimiento'], name='compra_detalle_ibfk_3'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='compra_detalle_ibfk_2'),
        Index('idx_cd_compra', 'id_compra'),
        Index('idx_cd_movimiento', 'id_movimiento'),
        Index('idx_cd_producto', 'id_producto')
    )

    id_compra_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_compra: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    id_movimiento: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    compras: Mapped['Compras'] = relationship('Compras', back_populates='compra_detalle')
    movimiento: Mapped['Movimiento'] = relationship('Movimiento', back_populates='compra_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='compra_detalle')


class DevolucionesClientes(Base):
    __tablename__ = 'devoluciones_clientes'
    __table_args__ = (
        ForeignKeyConstraint(['id_pedido_cliente'], ['pedidos_clientes.id_pedido_cliente'], name='devoluciones_clientes_ibfk_1'),
        Index('id_pedido_cliente', 'id_pedido_cliente')
    )

    id_devolucion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_devolucion: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    estatus: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(Text)

    pedidos_clientes: Mapped['PedidosClientes'] = relationship('PedidosClientes', back_populates='devoluciones_clientes')
    devolucion_cliente_detalle: Mapped[list['DevolucionClienteDetalle']] = relationship('DevolucionClienteDetalle', back_populates='devoluciones_clientes')


class DevolucionesProveedores(Base):
    __tablename__ = 'devoluciones_proveedores'
    __table_args__ = (
        ForeignKeyConstraint(['id_pedido_proveedor'], ['pedidos_proveedores.id_pedido_proveedor'], name='devoluciones_proveedores_ibfk_1'),
        Index('id_pedido_proveedor', 'id_pedido_proveedor')
    )

    id_devolucion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_proveedor: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_devolucion: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    estatus: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(Text)

    pedidos_proveedores: Mapped['PedidosProveedores'] = relationship('PedidosProveedores', back_populates='devoluciones_proveedores')
    devolucion_proveedor_detalle: Mapped[list['DevolucionProveedorDetalle']] = relationship('DevolucionProveedorDetalle', back_populates='devoluciones_proveedores')


class Envios(Base):
    __tablename__ = 'envios'
    __table_args__ = (
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='envios_ibfk_3'),
        ForeignKeyConstraint(['id_pedido_cliente'], ['pedidos_clientes.id_pedido_cliente'], name='envios_ibfk_1'),
        ForeignKeyConstraint(['id_vehiculo'], ['vehiculo.id_vehiculo'], name='envios_ibfk_2'),
        Index('id_empleado', 'id_empleado'),
        Index('idx_envio_vehiculo', 'id_vehiculo'),
        Index('uk_envio_pedido', 'id_pedido_cliente', unique=True)
    )

    id_envio: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_envio: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_pedido_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_vehiculo: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pendiente'"))

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='envios')
    pedidos_clientes: Mapped['PedidosClientes'] = relationship('PedidosClientes', back_populates='envios')
    vehiculo: Mapped['Vehiculo'] = relationship('Vehiculo', back_populates='envios')
    asignacion_transporte: Mapped[list['AsignacionTransporte']] = relationship('AsignacionTransporte', back_populates='envios')
    envio_detalle: Mapped[list['EnvioDetalle']] = relationship('EnvioDetalle', back_populates='envios')
    ruta_envio: Mapped[list['RutaEnvio']] = relationship('RutaEnvio', back_populates='envios')
    seguimiento_envio: Mapped[list['SeguimientoEnvio']] = relationship('SeguimientoEnvio', back_populates='envios')


class GuiaRemision(Base):
    __tablename__ = 'guia_remision'
    __table_args__ = (
        ForeignKeyConstraint(['id_conductor'], ['conductores.id_empleado'], name='guia_remision_ibfk_3'),
        ForeignKeyConstraint(['id_pedido_cliente'], ['pedidos_clientes.id_pedido_cliente'], name='guia_remision_ibfk_1'),
        ForeignKeyConstraint(['id_vehiculo'], ['vehiculo.id_vehiculo'], name='guia_remision_ibfk_2'),
        Index('id_pedido_cliente', 'id_pedido_cliente'),
        Index('idx_gr_conductor', 'id_conductor'),
        Index('idx_gr_vehiculo', 'id_vehiculo')
    )

    id_guia: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_guia: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_vehiculo: Mapped[int] = mapped_column(Integer, nullable=False)
    id_conductor: Mapped[int] = mapped_column(Integer, nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False)

    conductores: Mapped['Conductores'] = relationship('Conductores', back_populates='guia_remision')
    pedidos_clientes: Mapped['PedidosClientes'] = relationship('PedidosClientes', back_populates='guia_remision')
    vehiculo: Mapped['Vehiculo'] = relationship('Vehiculo', back_populates='guia_remision')
    guia_remision_detalle: Mapped[list['GuiaRemisionDetalle']] = relationship('GuiaRemisionDetalle', back_populates='guia_remision')


class MovimientoDetalle(Base):
    __tablename__ = 'movimiento_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_almacen'], ['almacenes.id_almacen'], name='movimiento_detalle_ibfk_3'),
        ForeignKeyConstraint(['id_movimiento'], ['movimiento.id_movimiento'], ondelete='CASCADE', name='movimiento_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='movimiento_detalle_ibfk_2'),
        Index('idx_md_almacen', 'id_almacen'),
        Index('idx_md_movimiento', 'id_movimiento'),
        Index('idx_md_producto', 'id_producto')
    )

    id_movimiento_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_movimiento: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', back_populates='movimiento_detalle')
    movimiento: Mapped['Movimiento'] = relationship('Movimiento', back_populates='movimiento_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='movimiento_detalle')


class PedidoClienteDetalle(Base):
    __tablename__ = 'pedido_cliente_detalle'
    __table_args__ = (
        CheckConstraint('(`cantidad` > 0)', name='pedido_cliente_detalle_chk_1'),
        ForeignKeyConstraint(['id_pedido_cliente'], ['pedidos_clientes.id_pedido_cliente'], ondelete='CASCADE', name='pedido_cliente_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='pedido_cliente_detalle_ibfk_2'),
        Index('idx_pcd_pedido', 'id_pedido_cliente'),
        Index('idx_pcd_producto', 'id_producto')
    )

    id_pedido_cliente_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    pedidos_clientes: Mapped['PedidosClientes'] = relationship('PedidosClientes', back_populates='pedido_cliente_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='pedido_cliente_detalle')


class PedidoProveedorDetalle(Base):
    __tablename__ = 'pedido_proveedor_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_pedido_proveedor'], ['pedidos_proveedores.id_pedido_proveedor'], ondelete='CASCADE', name='pedido_proveedor_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='pedido_proveedor_detalle_ibfk_2'),
        Index('id_pedido_proveedor', 'id_pedido_proveedor'),
        Index('id_producto', 'id_producto')
    )

    id_pedido_proveedor_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_proveedor: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    pedidos_proveedores: Mapped['PedidosProveedores'] = relationship('PedidosProveedores', back_populates='pedido_proveedor_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='pedido_proveedor_detalle')


class ProductosAlmacen(Base):
    __tablename__ = 'productos_almacen'
    __table_args__ = (
        CheckConstraint('(`stock` >= 0)', name='productos_almacen_chk_1'),
        ForeignKeyConstraint(['id_almacen'], ['almacenes.id_almacen'], name='productos_almacen_ibfk_2'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='productos_almacen_ibfk_1'),
        Index('idx_pa_almacen', 'id_almacen'),
        Index('idx_pa_producto', 'id_producto'),
        Index('uk_producto_almacen', 'id_producto', 'id_almacen', unique=True)
    )

    id_producto_almacen: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    stock_minimo: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    stock_maximo: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', back_populates='productos_almacen')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='productos_almacen')


class TrasladoInternoDetalle(Base):
    __tablename__ = 'traslado_interno_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='traslado_interno_detalle_ibfk_2'),
        ForeignKeyConstraint(['id_traslado'], ['traslados_internos.id_traslado'], ondelete='CASCADE', name='traslado_interno_detalle_ibfk_1'),
        Index('id_producto', 'id_producto'),
        Index('id_traslado', 'id_traslado')
    )

    id_traslado_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_traslado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    productos: Mapped['Productos'] = relationship('Productos', back_populates='traslado_interno_detalle')
    traslados_internos: Mapped['TrasladosInternos'] = relationship('TrasladosInternos', back_populates='traslado_interno_detalle')


class AsignacionTransporte(Base):
    __tablename__ = 'asignacion_transporte'
    __table_args__ = (
        ForeignKeyConstraint(['id_conductor'], ['conductores.id_empleado'], name='asignacion_transporte_ibfk_2'),
        ForeignKeyConstraint(['id_envio'], ['envios.id_envio'], name='asignacion_transporte_ibfk_1'),
        Index('id_envio', 'id_envio'),
        Index('idx_at_conductor', 'id_conductor')
    )

    id_asignacion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_envio: Mapped[int] = mapped_column(Integer, nullable=False)
    id_conductor: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_asignacion: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))

    conductores: Mapped['Conductores'] = relationship('Conductores', back_populates='asignacion_transporte')
    envios: Mapped['Envios'] = relationship('Envios', back_populates='asignacion_transporte')


class DevolucionClienteDetalle(Base):
    __tablename__ = 'devolucion_cliente_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_devolucion'], ['devoluciones_clientes.id_devolucion'], ondelete='CASCADE', name='devolucion_cliente_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='devolucion_cliente_detalle_ibfk_2'),
        Index('id_devolucion', 'id_devolucion'),
        Index('id_producto', 'id_producto')
    )

    id_devolucion_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_devolucion: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    devoluciones_clientes: Mapped['DevolucionesClientes'] = relationship('DevolucionesClientes', back_populates='devolucion_cliente_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='devolucion_cliente_detalle')


class DevolucionProveedorDetalle(Base):
    __tablename__ = 'devolucion_proveedor_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_devolucion'], ['devoluciones_proveedores.id_devolucion'], ondelete='CASCADE', name='devolucion_proveedor_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='devolucion_proveedor_detalle_ibfk_2'),
        Index('id_devolucion', 'id_devolucion'),
        Index('id_producto', 'id_producto')
    )

    id_devolucion_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_devolucion: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    devoluciones_proveedores: Mapped['DevolucionesProveedores'] = relationship('DevolucionesProveedores', back_populates='devolucion_proveedor_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='devolucion_proveedor_detalle')


class EnvioDetalle(Base):
    __tablename__ = 'envio_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_envio'], ['envios.id_envio'], ondelete='CASCADE', name='envio_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='envio_detalle_ibfk_2'),
        Index('id_envio', 'id_envio'),
        Index('id_producto', 'id_producto')
    )

    id_envio_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_envio: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    envios: Mapped['Envios'] = relationship('Envios', back_populates='envio_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='envio_detalle')


class GuiaRemisionDetalle(Base):
    __tablename__ = 'guia_remision_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_guia'], ['guia_remision.id_guia'], ondelete='CASCADE', name='guia_remision_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='guia_remision_detalle_ibfk_2'),
        Index('id_guia', 'id_guia'),
        Index('id_producto', 'id_producto')
    )

    id_guia_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_guia: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    guia_remision: Mapped['GuiaRemision'] = relationship('GuiaRemision', back_populates='guia_remision_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='guia_remision_detalle')


class RutaEnvio(Base):
    __tablename__ = 'ruta_envio'
    __table_args__ = (
        ForeignKeyConstraint(['id_envio'], ['envios.id_envio'], ondelete='CASCADE', name='ruta_envio_ibfk_2'),
        ForeignKeyConstraint(['id_ruta'], ['ruta.id_ruta'], name='ruta_envio_ibfk_1'),
        Index('idx_re_envio', 'id_envio'),
        Index('idx_re_ruta', 'id_ruta')
    )

    id_ruta_envio: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_ruta: Mapped[int] = mapped_column(Integer, nullable=False)
    id_envio: Mapped[int] = mapped_column(Integer, nullable=False)

    envios: Mapped['Envios'] = relationship('Envios', back_populates='ruta_envio')
    ruta: Mapped['Ruta'] = relationship('Ruta', back_populates='ruta_envio')


class SeguimientoEnvio(Base):
    __tablename__ = 'seguimiento_envio'
    __table_args__ = (
        ForeignKeyConstraint(['id_envio'], ['envios.id_envio'], ondelete='CASCADE', name='seguimiento_envio_ibfk_1'),
        Index('idx_se_envio', 'id_envio')
    )

    id_seguimiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_envio: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_seguimiento: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    estatus: Mapped[str] = mapped_column(String(20), nullable=False)
    ubicacion: Mapped[Optional[str]] = mapped_column(String(100))

    envios: Mapped['Envios'] = relationship('Envios', back_populates='seguimiento_envio')
