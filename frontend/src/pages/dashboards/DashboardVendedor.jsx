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

export default function DashboardVendedor() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/reportes/dashboard`, { headers: getAuthHeaders() }).then(r => r.json()),
      fetch(`${API}/clientes`, { headers: getAuthHeaders() }).then(r => r.json()),
      fetch(`${API}/productos`, { headers: getAuthHeaders() }).then(r => r.json()),
    ])
      .then(([reportes, clients, prods]) => {
        setData({ ...reportes, clientes: clients.total || 0, productos: Array.isArray(prods) ? prods.length : 0 });
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <p className="p-6">Cargando...</p>;
  if (!data) return <p className="p-6">Error al cargar datos</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Panel de Ventas</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card title="Clientes" value={data.clientes} color="border-blue-500" />
        <Card title="Productos" value={data.productos} color="border-green-500" />
        <Card title="Ventas del Mes" value={data.ventas?.ventas_mes || 0} subtitle={data.ventas?.monto_mes ? `$${parseFloat(data.ventas.monto_mes).toLocaleString()}` : ''} color="border-yellow-500" />
      </div>
      {data.ventas && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <Card title="Ventas Hoy" value={data.ventas.ventas_hoy} subtitle={`$${parseFloat(data.ventas.monto_hoy).toLocaleString()}`} color="border-blue-500" />
          <Card title="Ventas Semana" value={data.ventas.ventas_semana} subtitle={`$${parseFloat(data.ventas.monto_semana).toLocaleString()}`} color="border-green-500" />
        </div>
      )}
      {data.productos_mas_vendidos?.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="font-semibold mb-3">Productos Más Vendidos</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead><tr className="border-b text-left"><th className="pb-2 text-gray-500">Producto</th><th className="pb-2 text-gray-500">Unidades</th><th className="pb-2 text-gray-500">Monto</th></tr></thead>
              <tbody>
                {data.productos_mas_vendidos.map((p, i) => (
                  <tr key={i} className="border-b last:border-0"><td className="py-2">{p.nombre}</td><td className="py-2">{p.total_vendido}</td><td className="py-2">${parseFloat(p.monto_total).toLocaleString()}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      <div className="bg-blue-50 p-4 rounded-lg">
        <p className="text-blue-700 font-medium mb-2">Accesos rápidos:</p>
        <div className="flex gap-2">
          <a href="/clientes" className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">Clientes</a>
          <a href="/productos" className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700">Productos</a>
          <a href="/ventas" className="bg-yellow-600 text-white px-4 py-2 rounded text-sm hover:bg-yellow-700">Ventas</a>
        </div>
      </div>
    </div>
  );
}
