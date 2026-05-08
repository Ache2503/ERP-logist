# Guía de Desarrollo Frontend - ERP System

## 📋 Índice
1. [Tech Stack](#tech-stack)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Cómo Agregar un Nuevo Módulo](#cómo-agregar-un-nuevo-módulo)
4. [Componentes Reutilizables](#componentes-reutilizables)
5. [Patrones de Código](#patrones-de-código)
6. [Ejemplos Completos](#ejemplos-completos)

---

## 🛠 Tech Stack

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| React | 19.2.5 | UI Library |
| Vite | 8.0.10 | Build tool & dev server |
| Tailwind CSS | 3.4.19 | Estilos utilitarios |
| React Router DOM | 7.14.2 | Enrutamiento |
| PostCSS | 8.5.12 | Procesador CSS |

---

## 📁 Estructura del Proyecto

```
frontend/
├── public/                    # Archivos estáticos
├── src/
│   ├── assets/               # Imágenes, fuentes, etc.
│   ├── components/           # Componentes reutilizables
│   │   ├── DataTable.jsx    # Tabla genérica con paginación
│   │   ├── Layout.jsx       # Estructura principal (Sidebar + Header + Content)
│   │   ├── Sidebar.jsx      # Menú lateral de navegación
│   │   ├── Header.jsx       # Barra superior
│   │   ├── ClientesTable.jsx    # Tabla específica de clientes
│   │   ├── EmpleadosTable.jsx   # Tabla específica de empleados
│   │   └── FormBuilder.jsx      # (Pendiente) Constructor de formularios
│   ├── hooks/
│   │   └── useApi.js         # Hook personalizado para consumir API
│   ├── pages/
│   │   ├── Dashboard.jsx     # Página principal
│   │   ├── ClientesPage.jsx  # Página de clientes
│   │   ├── EmpleadosPage.jsx # Página de empleados
│   │   └── EmpleadosPages.jsx # (DUPLICADO - Eliminar)
│   ├── App.jsx               # Configuración de rutas
│   ├── main.jsx              # Entry point
│   ├── index.css             # Estilos globales + Tailwind
│   └── App.css               # Estilos específicos de App
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

---

## 🚀 Cómo Agregar un Nuevo Módulo

### Paso 1: Verificar el Endpoint en el Backend

Antes de empezar, asegúrate de que el endpoint existe en el backend. Consulta el README.md raíz para ver los endpoints disponibles.

Ejemplo: `/productos` debe responder a GET, POST, PUT, DELETE.

---

### Paso 2: Crear el Componente de Tabla

Crea un archivo en `src/components/` siguiendo el patrón `NombreTable.jsx`.

**Ejemplo: `ProductosTable.jsx`**

```jsx
import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_producto', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'codigo', label: 'Código' },
  { key: 'precio', label: 'Precio', render: (row) => `$${row.precio.toFixed(2)}` },
  { 
    key: 'estatus', 
    label: 'Estatus', 
    render: (row) => (
      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
        row.estatus === 'activo' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
      }`}>
        {row.estatus}
      </span>
    )
  },
  { key: 'fecha_registro', label: 'Fecha Registro' },
];

export default function ProductosTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/productos/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Listado de Productos ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nuevo Producto
        </button>
      </div>
      <DataTable
        columns={columnas}
        data={data}
        loading={loading}
        error={error}
        total={total}
        skip={skip}
        limit={limit}
        onPageChange={setSkip}
      />
    </div>
  );
}
```

---

### Paso 3: Crear la Página

Crea un archivo en `src/pages/` siguiendo el patrón `NombrePage.jsx`.

**Ejemplo: `ProductosPage.jsx`**

```jsx
import ProductosTable from '../components/ProductosTable';

export default function ProductosPage() {
  return <ProductosTable />;
}
```

---

### Paso 4: Agregar la Ruta en App.jsx

Edita `src/App.jsx` y agrega la nueva ruta:

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import EmpleadosPage from './pages/EmpleadosPage';
import ClientesPage from './pages/ClientesPage';
import ProductosPage from './pages/ProductosPage';  // ← NUEVO

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="empleados" element={<EmpleadosPage />} />
          <Route path="clientes" element={<ClientesPage />} />
          <Route path="productos" element={<ProductosPage />} />  {/* ← NUEVO */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

---

### Paso 5: Agregar al Menú Lateral (Sidebar)

Edita `src/components/Sidebar.jsx` y agrega el nuevo elemento al array `menuItems`:

```jsx
const menuItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/empleados', label: 'Empleados', icon: '👥' },
  { path: '/clientes', label: 'Clientes', icon: '🏢' },
  { path: '/productos', label: 'Productos', icon: '📦' },  // ← NUEVO
  { path: '/ventas', label: 'Ventas', icon: '💰' },
  { path: '/compras', label: 'Compras', icon: '🛒' },      // ← NUEVO
  { path: '/almacenes', label: 'Almacenes', icon: '🏭' },  // ← NUEVO
];
```

---

## 🧩 Componentes Reutilizables

### DataTable.jsx

Componente genérico para mostrar datos en tabla con paginación.

**Props:**

| Prop | Tipo | Descripción |
|------|------|-------------|
| `columns` | Array | Definición de columnas (ver formato abajo) |
| `data` | Array | Datos a mostrar |
| `loading` | Boolean | Estado de carga |
| `error` | String | Mensaje de error |
| `total` | Number | Total de registros |
| `skip` | Number | Registro inicial (paginación) |
| `limit` | Number | Registros por página |
| `onPageChange` | Function | Callback para cambiar página |

**Formato de columnas:**

```javascript
const columnas = [
  { 
    key: 'id_cliente',           // Clave en el objeto de datos
    label: 'ID',                 // Texto del encabezado
    render: (row) => row.id      // (Opcional) Función personalizada de renderizado
  },
  { 
    key: 'estatus', 
    label: 'Estatus',
    render: (row) => (
      <span className={row.estatus === 'activo' ? 'text-green-600' : 'text-red-600'}>
        {row.estatus}
      </span>
    )
  },
];
```

---

### useApi.js (Hook Personalizado)

Hook para consumir APIs con paginación automática.

**Uso:**

```javascript
const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/empleados/');
```

**Retorna:**

| Valor | Tipo | Descripción |
|-------|------|-------------|
| `data` | Array/Null | Datos recibidos de la API |
| `loading` | Boolean | `true` mientras carga |
| `error` | String/Null | Mensaje de error si falla |
| `total` | Number | Total de registros (para paginación) |
| `skip` | Number | Offset actual |
| `limit` | Number | Límite por página (default: 100) |
| `setSkip` | Function | Cambiar página: `setSkip(nuevo_skip)` |

**Opciones (segundo parámetro):**

```javascript
const { data, ... } = useApi('http://localhost:8000/endpoint/', {
  skip: 0,      // Valor inicial de skip
  limit: 50     // Cambiar límite de registros por página
});
```

---

### Layout.jsx

Estructura principal que envuelve todas las páginas.

```
┌─────────────────────────────────────────────┐
│  Sidebar (izquierda)  │   Main Content    │
│                      │                   │
│  - Dashboard         │  Header           │
│  - Empleados        │                   │
│  - Clientes         │  <Outlet />       │
│  ...                │  (Aquí se renderiza│
│                      │   la página)      │
└─────────────────────────────────────────────┘
```

Para agregar contenido fuera del `<Outlet />`, edita este componente.

---

## 🎨 Patrones de Código con Tailwind CSS

### Tablas

```jsx
<div className="overflow-x-auto bg-white shadow rounded">
  <table className="min-w-full divide-y divide-gray-200">
    <thead className="bg-gray-50">
      <tr>
        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
          Columna
        </th>
      </tr>
    </thead>
    <tbody className="bg-white divide-y divide-gray-200">
      {/* filas */}
    </tbody>
  </table>
</div>
```

### Botones

```jsx
// Primario
<button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
  Guardar
</button>

// Secundario
<button className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded">
  Cancelar
</button>

// Peligro
<button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded">
  Eliminar
</button>
```

### Badges / Estados

```jsx
<span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
  row.estatus === 'activo' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
}`}>
  {row.estatus}
</span>
```

### Formularios (Próximamente con FormBuilder)

```jsx
<div className="mb-4">
  <label className="block text-sm font-medium text-gray-700 mb-1">
    Nombre
  </label>
  <input 
    type="text" 
    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
    placeholder="Ingresa el nombre"
  />
</div>
```

---

## 📝 Ejemplos Completos

### Ejemplo 1: Módulo de Marcas (Simple)

**Paso 1: `src/components/MarcasTable.jsx`**

```jsx
import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_marca', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'fecha_registro', label: 'Fecha Registro' },
];

export default function MarcasTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/marcas/');

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Listado de Marcas ({total})</h2>
      <DataTable
        columns={columnas}
        data={data}
        loading={loading}
        error={error}
        total={total}
        skip={skip}
        limit={limit}
        onPageChange={setSkip}
      />
    </div>
  );
}
```

**Paso 2: `src/pages/MarcasPage.jsx`**

```jsx
import MarcasTable from '../components/MarcasTable';

export default function MarcasPage() {
  return <MarcasTable />;
}
```

**Paso 3: Actualizar `App.jsx`**

```jsx
import MarcasPage from './pages/MarcasPage';

// En el componente App, dentro de <Route path="/" element={<Layout />}>
<Route path="marcas" element={<MarcasPage />} />
```

**Paso 4: Actualizar `Sidebar.jsx`**

```jsx
const menuItems = [
  // ... otros items
  { path: '/marcas', label: 'Marcas', icon: '🏷️' },
];
```

---

### Ejemplo 2: Módulo de Ventas (Con más columnas)

**`src/components/VentasTable.jsx`**

```jsx
import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_venta', label: 'ID' },
  { key: 'numero_venta', label: 'Número' },
  { 
    key: 'id_cliente', 
    label: 'Cliente',
    render: (row) => `Cliente #${row.id_cliente}`  // En el futuro: mostrar nombre
  },
  { 
    key: 'total', 
    label: 'Total',
    render: (row) => `$${row.total ? row.total.toFixed(2) : '0.00'}`
  },
  { 
    key: 'estatus', 
    label: 'Estatus',
    render: (row) => (
      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
        row.estatus === 'completada' ? 'bg-green-100 text-green-800' : 
        row.estatus === 'pendiente' ? 'bg-yellow-100 text-yellow-800' :
        'bg-gray-100 text-gray-800'
      }`}>
        {row.estatus}
      </span>
    )
  },
  { key: 'fecha_venta', label: 'Fecha' },
];

export default function VentasTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/ventas/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Listado de Ventas ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nueva Venta
        </button>
      </div>
      <DataTable
        columns={columnas}
        data={data}
        loading={loading}
        error={error}
        total={total}
        skip={skip}
        limit={limit}
        onPageChange={setSkip}
      />
    </div>
  );
}
```

---

## ⚠️ Notas Importantes

### 1. Limpiar Archivos Duplicados
Hay un archivo duplicado: `EmpleadosPages.jsx` (con 's' al final). Eliminarlo:
```bash
rm /home/axel-michael/Documentos/proyecto-erp/frontend/src/pages/EmpleadosPages.jsx
```

### 2. FormBuilder.jsx está vacío
El archivo `FormBuilder.jsx` está creado pero vacío. Se planea usar para generar formularios dinámicos basados en esquemas.

### 3. API Base URL
Actualmente la URL de la API está hardcodeada en cada componente (`http://localhost:8000`). 
**Recomendación:** Crear un archivo de configuración:

```javascript
// src/config.js
export const API_URL = 'http://localhost:8000';
```

Y usarlo:
```javascript
import { API_URL } from '../config';
const { data, ... } = useApi(`${API_URL}/productos/`);
```

### 4. Manejo de Fechas
Las fechas vienen como strings desde el backend. Para formatear:
```javascript
{ key: 'fecha_registro', label: 'Fecha', render: (row) => new Date(row.fecha_registro).toLocaleDateString('es-MX') }
```

---

## 🔗 Endpoints Disponibles (Backend)

Consulta el archivo `/README.md` en la raíz del proyecto para ver todos los endpoints disponibles.

Algunos ejemplos:
- `http://localhost:8000/clientes/`
- `http://localhost:8000/empleados/`
- `http://localhost:8000/productos/`
- `http://localhost:8000/marcas/`
- `http://localhost:8000/categorias/`
- `http://localhost:8000/ventas/`
- `http://localhost:8000/compras/`
- `http://localhost:8000/inventario/`
- `http://localhost:8000/logistica/`
- `http://localhost:8000/pedidos-clientes/`

---

## 🚦 Comandos Útiles

```bash
# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev

# Construir para producción
npm run build

# Linting
npm run lint

# Vista previa de producción
npm run preview
```

---

## 📞 Contacto y Soporte

Para dudas sobre el desarrollo del frontend, consultar:
- Este archivo: `FRONTEND_GUIDE.md`
- README principal: `/README.md`
- Documentación de React: https://react.dev
- Documentación de Tailwind: https://tailwindcss.com/docs
- Documentación de Vite: https://vitejs.dev
