import { NavLink } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const ALL_MENU = [
  { path: '/', label: 'Dashboard' },
  { path: '/empleados', label: 'Empleados' },
  { path: '/clientes', label: 'Clientes' },
  { path: '/productos', label: 'Productos' },
  { path: '/marcas', label: 'Marcas' },
  { path: '/categorias', label: 'Categorias' },
  { path: '/unidades-medida', label: 'Unidades' },
  { path: '/almacenes', label: 'Almacenes' },
  { path: '/proveedores', label: 'Proveedores' },
  { path: '/ventas', label: 'Ventas' },
  { path: '/compras', label: 'Compras' },
  { path: '/pedidos-clientes', label: 'Pedidos' },
  { path: '/inventario', label: 'Inventario' },
  { path: '/logistica', label: 'Logistica' },
  { path: '/vehiculos', label: 'Vehiculos' },
  { path: '/conductores', label: 'Transportistas' },
  { path: '/tipos-vehiculos', label: 'Tipos Veh.' },
  { path: '/roles', label: 'Roles' },
  { path: '/permisos', label: 'Permisos' },
  { path: '/reportes', label: 'Reportes' },
];

const ROLE_MENU = {
  Administrador: ALL_MENU,
  Vendedor: [
    { path: '/', label: 'Dashboard' },
    { path: '/clientes', label: 'Clientes' },
    { path: '/productos', label: 'Productos' },
    { path: '/ventas', label: 'Ventas' },
    { path: '/pedidos-clientes', label: 'Pedidos' },
  ],
  Almacenista: [
    { path: '/', label: 'Dashboard' },
    { path: '/almacenes', label: 'Almacenes' },
    { path: '/productos', label: 'Productos' },
    { path: '/inventario', label: 'Inventario' },
  ],
  Contador: [
    { path: '/', label: 'Dashboard' },
    { path: '/compras', label: 'Compras' },
    { path: '/proveedores', label: 'Proveedores' },
    { path: '/ventas', label: 'Ventas' },
  ],
  Gerente: [
    { path: '/', label: 'Dashboard' },
    { path: '/empleados', label: 'Empleados' },
    { path: '/clientes', label: 'Clientes' },
    { path: '/productos', label: 'Productos' },
    { path: '/ventas', label: 'Ventas' },
    { path: '/compras', label: 'Compras' },
    { path: '/inventario', label: 'Inventario' },
    { path: '/reportes', label: 'Reportes' },
  ],
  Transportista: [
    { path: '/', label: 'Dashboard' },
    { path: '/logistica', label: 'Logistica' },
    { path: '/vehiculos', label: 'Vehiculos' },
    { path: '/conductores', label: 'Transportistas' },
  ],
};

export default function Sidebar() {
  const { empleado } = useAuth();
  const cargo = empleado?.cargo || 'Vendedor';
  const menuItems = ROLE_MENU[cargo] || ROLE_MENU.Vendedor;

  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen p-4">
      <h2 className="text-2xl font-bold mb-6">ERP System</h2>
      <p className="text-xs text-gray-400 mb-4 px-4">{cargo}</p>
      <nav>
        <ul className="space-y-2">
          {menuItems.map(item => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                end={item.path === '/'}  
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-2 rounded transition-colors ${
                    isActive ? 'bg-blue-600 text-white' : 'hover:bg-gray-700'
                  }`
                }
              >
                <span>{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
