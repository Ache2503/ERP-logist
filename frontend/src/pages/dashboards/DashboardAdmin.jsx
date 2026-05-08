import { useState, useEffect } from 'react';
import { getAuthHeaders } from '../../hooks/useApi';
import API_BASE from '../../config';

const API = API_BASE;

function Card({ title, value, subtitle, color }) {
  return (
    <div className={`bg-white p-6 rounded-lg shadow border-l-4 ${color}`}>
      <p className="text-sm text-gray-500">{title}</p>
      <p className="text-3xl font-bold">{value}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
    </div>
  );
}

export default function DashboardAdmin() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/reportes/dashboard`, { headers: getAuthHeaders() })
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <p className="p-6">Cargando estadísticas...</p>;

  const { empleados, ventas, inventario, financiero, productos_mas_vendidos } = data || {};

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Panel de Administración</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <Card title="Empleados" value={empleados?.total || '-'} subtitle={`${empleados?.activos || 0} activos`} color="border-blue-500" />
        <Card title="Clientes" value={data?.clientes || '-'} color="border-green-500" />
        <Card title="Productos" value={inventario?.total_productos || '-'} subtitle={`${inventario?.productos_bajo_stock || 0} bajo stock`} color="border-yellow-500" />
        <Card title="Transportistas" value={empleados?.por_cargo?.find(c => c.cargo === 'Transportista')?.total || 0} color="border-purple-500" />
      </div>
      {ventas && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <Card title="Ventas Hoy" value={ventas.ventas_hoy} subtitle={`$${parseFloat(ventas.monto_hoy).toLocaleString()}`} color="border-blue-500" />
          <Card title="Ventas Semana" value={ventas.ventas_semana} subtitle={`$${parseFloat(ventas.monto_semana).toLocaleString()}`} color="border-green-500" />
          <Card title="Ventas Mes" value={ventas.ventas_mes} subtitle={`$${parseFloat(ventas.monto_mes).toLocaleString()}`} color="border-purple-500" />
        </div>
      )}
      {financiero && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card title="Ventas Totales" value={`$${parseFloat(financiero.ventas_totales).toLocaleString()}`} color="border-green-500" />
          <Card title="Compras Totales" value={`$${parseFloat(financiero.compras_totales).toLocaleString()}`} color="border-red-500" />
          <Card title="Ganancia Estimada" value={`$${parseFloat(financiero.ganancia_estimada).toLocaleString()}`} color="border-blue-500" />
          <Card title="Ventas del Mes" value={`$${parseFloat(financiero.ventas_mes_actual).toLocaleString()}`} color="border-purple-500" />
        </div>
      )}
      {productos_mas_vendidos?.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold mb-3">Productos Más Vendidos</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead><tr className="border-b text-left"><th className="pb-2 text-gray-500">Producto</th><th className="pb-2 text-gray-500">Vendidos</th><th className="pb-2 text-gray-500">Monto</th></tr></thead>
              <tbody>
                {productos_mas_vendidos.map((p, i) => (
                  <tr key={i} className="border-b last:border-0">
                    <td className="py-2">{p.nombre}</td>
                    <td className="py-2">{p.total_vendido}</td>
                    <td className="py-2">${parseFloat(p.monto_total).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
