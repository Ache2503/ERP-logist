import { useState, useEffect } from 'react';
import { getAuthHeaders } from '../../hooks/useApi';
import { useAuth } from '../../hooks/useAuth';
import API_BASE from '../../config';

const API = API_BASE;

function Card({ title, value, subtitle, color }) {
  return (
    <div className={`bg-white p-4 rounded-lg shadow border-l-4 ${color}`}>
      <p className="text-xs text-gray-500">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
    </div>
  );
}

export default function DashboardGerente() {
  const { empleado } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/reportes/dashboard`, { headers: getAuthHeaders() })
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <p className="p-6">Cargando indicadores...</p>;

  const { empleados, ventas, inventario, financiero, productos_mas_vendidos } = data || {};

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Panel Gerencial</h2>
        <span className="text-gray-500">Bienvenido, {empleado?.nombre}</span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
        <Card title="Empleados" value={empleados?.total || 0} subtitle={`${empleados?.activos || 0} activos`} color="border-blue-500" />
        <Card title="Clientes" value={data?.clientes || 0} color="border-green-500" />
        <Card title="Productos" value={inventario?.total_productos || 0} color="border-yellow-500" />
        <Card title="Ventas Mes" value={ventas?.ventas_mes || 0} subtitle={ventas?.monto_mes ? `$${parseFloat(ventas.monto_mes).toLocaleString()}` : ''} color="border-purple-500" />
        <Card title="Compras" value={data?.compras || 0} color="border-red-500" />
        <Card title="Inventario" value={inventario?.total_en_stock || 0} color="border-indigo-500" />
      </div>

      {financiero && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card title="Ventas Totales" value={`$${parseFloat(financiero.ventas_totales).toLocaleString()}`} color="border-green-500" />
          <Card title="Compras Totales" value={`$${parseFloat(financiero.compras_totales).toLocaleString()}`} color="border-red-500" />
          <Card title="Ganancia Estimada" value={`$${parseFloat(financiero.ganancia_estimada).toLocaleString()}`} subtitle={financiero.ganancia_estimada >= 0 ? ' positiva' : ' negativa'} color={financiero.ganancia_estimada >= 0 ? 'border-green-600' : 'border-red-600'} />
          <Card title="Valor Inventario" value={`$${parseFloat(inventario?.valor_total_inventario || 0).toLocaleString()}`} color="border-blue-500" />
        </div>
      )}

      {ventas?.ventas_por_periodo?.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="font-semibold mb-3">Ventas por Mes</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead><tr className="border-b text-left"><th className="pb-2 text-gray-500">Período</th><th className="pb-2 text-gray-500">Ventas</th><th className="pb-2 text-gray-500">Monto</th></tr></thead>
              <tbody>
                {ventas.ventas_por_periodo.map((p, i) => (
                  <tr key={i} className="border-b last:border-0"><td className="py-2">{p.periodo}</td><td className="py-2">{p.total_ventas}</td><td className="py-2">${parseFloat(p.monto_total).toLocaleString()}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {empleados?.por_cargo?.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold mb-3">Empleados por Cargo</h3>
            {empleados.por_cargo.map((c, i) => (
              <div key={i} className="flex justify-between text-sm py-2 border-b last:border-0">
                <span>{c.cargo}</span>
                <span className="font-medium">{c.total}</span>
              </div>
            ))}
          </div>
        )}
        {productos_mas_vendidos?.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold mb-3">Productos Más Vendidos</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead><tr className="border-b text-left"><th className="pb-2 text-gray-500">Producto</th><th className="pb-2 text-gray-500">Vendidos</th></tr></thead>
                <tbody>
                  {productos_mas_vendidos.map((p, i) => (
                    <tr key={i} className="border-b last:border-0"><td className="py-2">{p.nombre}</td><td className="py-2">{p.total_vendido}</td></tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {inventario?.productos_bajo_stock > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-700 font-medium">⚠ {inventario.productos_bajo_stock} producto(s) con stock bajo</p>
        </div>
      )}

      <div className="bg-purple-50 p-4 rounded-lg">
        <p className="text-purple-700">Resumen ejecutivo del sistema — todos los indicadores clave en un solo vistazo</p>
      </div>
    </div>
  );
}
