# 📘 DICCIONARIO DE DATOS

## Base de Datos: gestion

---

## 🎯 Descripción

Este diccionario de datos documenta la estructura de la base de datos "gestion", incluyendo tablas, campos, tipos de datos, llaves primarias y foráneas, así como sus descripciones.

---

# 👨‍💼 Tabla: empleados

| Campo                   | Tipo         | PK | FK | NN | UQ | Descripción                      |
| ----------------------- | ------------ | -- | -- | -- | -- | -------------------------------- |
| id_empleado             | INT          | SI | NO | SI | NO | Identificador único del empleado |
| nombre                  | VARCHAR(100) | NO | NO | SI | NO | Nombre del empleado              |
| apellido                | VARCHAR(100) | NO | NO | SI | NO | Apellido del empleado            |
| direccion               | VARCHAR(255) | NO | NO | NO | NO | Dirección                        |
| email                   | VARCHAR(100) | NO | NO | NO | SI | Correo electrónico               |
| telefono                | VARCHAR(20)  | NO | NO | NO | NO | Teléfono                         |
| rfc                     | VARCHAR(20)  | NO | NO | NO | SI | RFC                              |
| numero_seguridad_social | VARCHAR(20)  | NO | NO | NO | SI | NSS                              |
| cargo                   | VARCHAR(50)  | NO | NO | NO | NO | Puesto                           |
| estatus                 | VARCHAR(20)  | NO | NO | NO | NO | Estado                           |
| fecha_registro          | DATE         | NO | NO | NO | NO | Fecha de registro                |

---

# 👥 Tabla: clientes

| Campo          | Tipo         | PK | FK | NN | UQ | Descripción                     |
| -------------- | ------------ | -- | -- | -- | -- | ------------------------------- |
| id_cliente     | INT          | SI | NO | SI | NO | Identificador único del cliente |
| nombre         | VARCHAR(100) | NO | NO | SI | NO | Nombre                          |
| apellido       | VARCHAR(100) | NO | NO | NO | NO | Apellido                        |
| direccion      | VARCHAR(255) | NO | NO | NO | NO | Dirección                       |
| email          | VARCHAR(100) | NO | NO | NO | NO | Correo                          |
| telefono       | VARCHAR(20)  | NO | NO | NO | NO | Teléfono                        |
| rfc            | VARCHAR(20)  | NO | NO | NO | NO | RFC                             |
| estatus        | VARCHAR(20)  | NO | NO | NO | NO | Estado                          |
| fecha_registro | DATE         | NO | NO | NO | NO | Fecha de registro               |

---

# 📦 Tabla: productos

| Campo        | Tipo          | PK | FK | NN | UQ | Descripción                |
| ------------ | ------------- | -- | -- | -- | -- | -------------------------- |
| id_producto  | INT           | SI | NO | SI | NO | Identificador del producto |
| nombre       | VARCHAR(100)  | NO | NO | SI | NO | Nombre del producto        |
| descripcion  | TEXT          | NO | NO | NO | NO | Descripción                |
| precio       | DECIMAL(10,2) | NO | NO | NO | NO | Precio                     |
| id_categoria | INT           | NO | SI | NO | NO | Relación con categorías    |
| id_marca     | INT           | NO | SI | NO | NO | Relación con marcas        |

---

# 🏬 Tabla: almacenes

| Campo           | Tipo         | PK | FK | NN | UQ | Descripción               |
| --------------- | ------------ | -- | -- | -- | -- | ------------------------- |
| id_almacen      | INT          | SI | NO | SI | NO | Identificador del almacén |
| nombre          | VARCHAR(100) | NO | NO | SI | NO | Nombre                    |
| direccion       | VARCHAR(255) | NO | NO | NO | NO | Dirección                 |
| id_tipo_almacen | INT          | NO | SI | NO | NO | Tipo de almacén           |

---

# 📊 Tabla: inventario

| Campo         | Tipo | PK | FK | NN | UQ | Descripción      |
| ------------- | ---- | -- | -- | -- | -- | ---------------- |
| id_inventario | INT  | SI | NO | SI | NO | Identificador    |
| id_producto   | INT  | NO | SI | NO | NO | Producto         |
| id_almacen    | INT  | NO | SI | NO | NO | Almacén          |
| cantidad      | INT  | NO | NO | SI | NO | Stock disponible |

---

# 🚚 Tabla: traslado

| Campo              | Tipo        | PK | FK | NN | UQ | Descripción     |
| ------------------ | ----------- | -- | -- | -- | -- | --------------- |
| id_traslado        | INT         | SI | NO | SI | NO | Identificador   |
| fecha              | DATE        | NO | NO | NO | NO | Fecha           |
| id_almacen_origen  | INT         | NO | SI | NO | NO | Almacén origen  |
| id_almacen_destino | INT         | NO | SI | NO | NO | Almacén destino |
| estatus            | VARCHAR(20) | NO | NO | NO | NO | Estado          |
| observaciones      | TEXT        | NO | NO | NO | NO | Observaciones   |

---

# 🔗 RELACIONES PRINCIPALES

* productos.id_categoria → categorias.id_categoria
* productos.id_marca → marcas.id_marca
* almacenes.id_tipo_almacen → tipos_almacen.id_tipo_almacen
* inventario.id_producto → productos.id_producto
* inventario.id_almacen → almacenes.id_almacen
* traslado.id_almacen_origen → almacenes.id_almacen
* traslado.id_almacen_destino → almacenes.id_almacen

---

# 🧠 NOTAS

* PK: Llave primaria
* FK: Llave foránea
* NN: Not Null
* UQ: Unique

Este documento sirve como base para desarrollo, mantenimiento y auditoría del sistema.

---

# 📜 REGLAS DE NEGOCIO

## 👨‍💼 Empleados

* Un empleado debe tener un **correo único**.
* El RFC y el número de seguridad social no pueden repetirse.
* Un empleado puede estar **activo o inactivo**.
* Todo empleado debe registrarse con una fecha de alta.

---

## 👥 Clientes

* Un cliente puede estar activo o inactivo.
* El RFC puede utilizarse para facturación.
* Un cliente puede existir sin compras registradas.

---

## 📦 Productos

* Todo producto debe pertenecer a **una categoría**.
* Todo producto debe estar asociado a **una marca**.
* Un producto puede existir en múltiples almacenes.
* El precio debe ser mayor o igual a 0.

---

## 🏬 Almacenes

* Todo almacén debe tener un tipo asignado.
* Un almacén puede contener múltiples productos.
* Un almacén puede ser origen o destino de traslados.

---

## 📊 Inventario

* No puede existir inventario sin producto ni almacén.
* La cantidad de inventario no puede ser negativa.
* Un producto puede tener diferentes cantidades en distintos almacenes.

---

## 🚚 Traslados

* Todo traslado debe tener un almacén origen y destino.
* El almacén origen y destino no deben ser el mismo.
* Un traslado puede tener múltiples productos asociados.
* El estatus del traslado puede ser:

  * pendiente
  * en_proceso
  * completado
  * cancelado

---

## 🔗 Integridad General

* Todas las relaciones deben respetar integridad referencial (FOREIGN KEY).
* No se debe eliminar un registro si tiene dependencias activas.
* Se recomienda usar borrado lógico (estatus) en lugar de eliminación física.

---

## 🧠 Reglas Operativas

* Todo movimiento de inventario debe registrarse.
* Los traslados deben actualizar automáticamente el inventario.
* Se debe poder auditar cualquier cambio en el sistema.

---

## 📌 Notas finales

Estas reglas garantizan consistencia, integridad y control del sistema, permitiendo escalabilidad y fácil mantenimiento.

---

# 🔗 CARDINALIDAD DE RELACIONES

A continuación se describen las relaciones entre tablas indicando su cardinalidad:

## 📦 Productos

* categorias (1) ──── (N) productos
  Una categoría puede tener muchos productos, pero un producto solo pertenece a una categoría.

* marcas (1) ──── (N) productos
  Una marca puede tener muchos productos, pero un producto solo pertenece a una marca.

---

## 🏬 Almacenes e Inventario

* almacenes (1) ──── (N) inventario
  Un almacén puede tener muchos registros de inventario.

* productos (1) ──── (N) inventario
  Un producto puede estar en muchos almacenes.

👉 Esto genera una relación **N:M entre productos y almacenes**, resuelta mediante la tabla inventario.

---

## 🚚 Traslados

* almacenes (1) ──── (N) traslado (origen)
* almacenes (1) ──── (N) traslado (destino)

Un almacén puede participar en muchos traslados como origen o destino.

---

## 📦 Detalle de Traslado

* traslado (1) ──── (N) detalle_traslado
  Un traslado puede tener múltiples productos.

* productos (1) ──── (N) detalle_traslado
  Un producto puede aparecer en múltiples traslados.

👉 Esto genera una relación **N:M entre traslado y productos**, resuelta mediante detalle_traslado.

---

## 🗂️ Categorías

* categoria_padre (1) ──── (N) categorias
  Una categoría padre puede tener muchas subcategorías.

---

## 🏬 Tipos de Almacén

* tipos_almacen (1) ──── (N) almacenes
  Un tipo de almacén puede clasificar múltiples almacenes.

---

## 👥 Clientes (potencial expansión)

* clientes (1) ──── (N) pedidos/ventas
  Un cliente puede realizar múltiples operaciones (pendiente de implementación).

---

## 👨‍💼 Empleados (potencial expansión)

* empleados (1) ──── (N) operaciones
  Un empleado puede gestionar múltiples acciones dentro del sistema.

---

## 🧠 Interpretación general

* Relaciones **1:N** son predominantes en el modelo.
* Relaciones **N:M** están correctamente normalizadas mediante tablas intermedias:

  * inventario
  * detalle_traslado

Esto asegura:

* Escalabilidad
* Integridad de datos
* Flexibilidad para futuras funcionalidades

---

## ✅ Conclusión

El modelo relacional presenta una estructura sólida, cumpliendo con buenas prácticas de diseño de bases de datos y permitiendo su implementación en sistemas empresariales reales.
