import { NavLink } from 'react-router-dom';

const menuItems = [
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
];

export default function Sidebar() {
  console.log('Sidebar rendering...');
  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen p-4">
      <h2 className="text-2xl font-bold mb-6">ERP System</h2>
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
