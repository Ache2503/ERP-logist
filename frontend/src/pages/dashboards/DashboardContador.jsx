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

export default function DashboardContador() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/reportes/financiero`, { headers: getAuthHeaders() }).then(r => r.json()),
      fetch(`${API}/reportes/ventas`, { headers: getAuthHeaders() }).then(r => r.json()),
      fetch(`${API}/compras`, { headers: getAuthHeaders() }).then(r => r.json()),
      fetch(`${API}/proveedores`, { headers: getAuthHeaders() }).then(r => r.json()),
      fetch(`${API}/ventas`, { headers: getAuthHeaders() }).then(r => r.json()),
    ])
      .then(([financiero, ventas, compras, provs, ventasList]) => {
        setData({
          financiero,
          ventas,
          compras: compras.total || 0,
          proveedores: provs.total || 0,
          ventasCount: ventasList.total || 0,
        });
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <p className="p-6">Cargando...</p>;
  if (!data) return <p className="p-6">Error al cargar datos</p>;

  const { financiero, ventas, compras, proveedores, ventasCount } = data;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Panel de Contabilidad</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <Card title="Compras" value={compras} color="border-red-500" />
        <Card title="Proveedores" value={proveedores} color="border-green-500" />
        <Card title="Ventas" value={ventasCount} color="border-blue-500" />
        <Card title="Ventas del Mes" value={ventas?.ventas_mes || 0} subtitle={ventas?.monto_mes ? `$${parseFloat(ventas.monto_mes).toLocaleString()}` : ''} color="border-purple-500" />
      </div>
      {financiero && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card title="Ventas Totales" value={`$${parseFloat(financiero.ventas_totales).toLocaleString()}`} color="border-green-500" />
          <Card title="Compras Totales" value={`$${parseFloat(financiero.compras_totales).toLocaleString()}`} color="border-red-500" />
          <Card title="Ganancia Estimada" value={`$${parseFloat(financiero.ganancia_estimada).toLocaleString()}`} color="border-blue-500" />
          <Card title="Compras del Mes" value={`$${parseFloat(financiero.compras_mes_actual).toLocaleString()}`} color="border-yellow-500" />
        </div>
      )}
      {ventas?.ventas_por_periodo?.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="font-semibold mb-3">Ventas por Período</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead><tr className="border-b text-left"><th className="pb-2 text-gray-500">Periodo</th><th className="pb-2 text-gray-500">Ventas</th><th className="pb-2 text-gray-500">Monto</th><th className="pb-2 text-gray-500">Promedio</th></tr></thead>
              <tbody>
                {ventas.ventas_por_periodo.map((p, i) => (
                  <tr key={i} className="border-b last:border-0">
                    <td className="py-2">{p.periodo}</td>
                    <td className="py-2">{p.total_ventas}</td>
                    <td className="py-2">${parseFloat(p.monto_total).toLocaleString()}</td>
                    <td className="py-2">${parseFloat(p.promedio_por_venta).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      <div className="bg-yellow-50 p-4 rounded-lg">
        <p className="text-yellow-700 font-medium mb-2">Accesos rápidos:</p>
        <div className="flex gap-2">
          <a href="/compras" className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">Compras</a>
          <a href="/proveedores" className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700">Proveedores</a>
          <a href="/ventas" className="bg-yellow-600 text-white px-4 py-2 rounded text-sm hover:bg-yellow-700">Ventas</a>
        </div>
      </div>
    </div>
  );
}
