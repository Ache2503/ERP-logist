import { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { getAuthHeaders } from '../hooks/useApi';

const API = 'http://localhost:8000';

function StatCard({ title, value, subtitle, color }) {
  return (
    <div className={`bg-white rounded-xl shadow-sm border-l-4 ${color} p-5`}>
      <p className="text-sm text-gray-500 font-medium">{title}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
    </div>
  );
}

function TableCard({ title, data, columns }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-5">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              {columns.map(col => (
                <th key={col.key} className="pb-2 font-medium text-gray-500">{col.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.length === 0 ? (
              <tr><td colSpan={columns.length} className="py-4 text-center text-gray-400">Sin datos</td></tr>
            ) : data.map((row, i) => (
              <tr key={i} className="border-b last:border-0 hover:bg-gray-50">
                {columns.map(col => (
                  <td key={col.key} className="py-2">{col.render ? col.render(row) : row[col.key]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default function ReportesPage() {
  const { empleado } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/reportes/dashboard`, { headers: getAuthHeaders() })
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6 text-center text-gray-500">Cargando reportes...</div>;
  if (!data) return <div className="p-6 text-center text-gray-500">Error al cargar reportes</div>;

  const { ventas, inventario, empleados: emp, financiero, productos_mas_vendidos } = data;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Reportes y Estadísticas</h1>

      {ventas && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <StatCard title="Ventas Hoy" value={ventas.ventas_hoy} subtitle={`$${parseFloat(ventas.monto_hoy).toLocaleString()}`} color="border-blue-500" />
            <StatCard title="Ventas Semana" value={ventas.ventas_semana} subtitle={`$${parseFloat(ventas.monto_semana).toLocaleString()}`} color="border-green-500" />
            <StatCard title="Ventas Mes" value={ventas.ventas_mes} subtitle={`$${parseFloat(ventas.monto_mes).toLocaleString()}`} color="border-purple-500" />
            <StatCard title="Promedio/Venta" value={ventas.ventas_por_periodo?.length ? `$${parseFloat(ventas.ventas_por_periodo[ventas.ventas_por_periodo.length - 1]?.promedio_por_venta || 0).toLocaleString()}` : '-'} color="border-yellow-500" />
          </div>
          {ventas.ventas_por_periodo?.length > 0 && (
            <TableCard
              title="Ventas por Mes"
              data={ventas.ventas_por_periodo}
              columns={[
                { key: 'periodo', label: 'Período' },
                { key: 'total_ventas', label: 'Ventas' },
                { key: 'monto_total', label: 'Monto Total', render: r => `$${parseFloat(r.monto_total).toLocaleString()}` },
                { key: 'promedio_por_venta', label: 'Promedio', render: r => `$${parseFloat(r.promedio_por_venta).toLocaleString()}` },
              ]}
            />
          )}
        </>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {inventario && (
          <div className="bg-white rounded-xl shadow-sm p-5">
            <h3 className="text-lg font-semibold mb-4">Inventario</h3>
            <div className="grid grid-cols-2 gap-4">
              <StatCard title="Productos" value={inventario.total_productos} color="border-indigo-500" />
              <StatCard title="Unidades en Stock" value={inventario.total_en_stock} color="border-teal-500" />
              <StatCard title="Productos Bajo Stock" value={inventario.productos_bajo_stock} color="border-red-500" />
              <StatCard title="Valor Total" value={`$${parseFloat(inventario.valor_total_inventario).toLocaleString()}`} color="border-green-500" />
            </div>
          </div>
        )}

        {emp && (
          <div className="bg-white rounded-xl shadow-sm p-5">
            <h3 className="text-lg font-semibold mb-4">Empleados</h3>
            <div className="grid grid-cols-2 gap-4">
              <StatCard title="Total" value={emp.total} color="border-blue-500" />
              <StatCard title="Activos" value={emp.activos} color="border-green-500" />
              <StatCard title="Inactivos" value={emp.inactivos} color="border-red-500" />
            </div>
            {emp.por_cargo?.length > 0 && (
              <div className="mt-4">
                <p className="text-sm font-medium text-gray-500 mb-2">Por Cargo</p>
                {emp.por_cargo.map((c, i) => (
                  <div key={i} className="flex justify-between text-sm py-1 border-b last:border-0">
                    <span>{c.cargo}</span>
                    <span className="font-medium">{c.total}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {financiero && (
          <div className="bg-white rounded-xl shadow-sm p-5">
            <h3 className="text-lg font-semibold mb-4">Resumen Financiero</h3>
            <div className="grid grid-cols-2 gap-4">
              <StatCard title="Ventas Totales" value={`$${parseFloat(financiero.ventas_totales).toLocaleString()}`} color="border-green-500" />
              <StatCard title="Compras Totales" value={`$${parseFloat(financiero.compras_totales).toLocaleString()}`} color="border-red-500" />
              <StatCard title="Ganancia Estimada" value={`$${parseFloat(financiero.ganancia_estimada).toLocaleString()}`} color="border-blue-500" />
              <StatCard title="Ventas Mes Actual" value={`$${parseFloat(financiero.ventas_mes_actual).toLocaleString()}`} color="border-purple-500" />
            </div>
          </div>
        )}

        {productos_mas_vendidos?.length > 0 && (
          <TableCard
            title="Productos Más Vendidos"
            data={productos_mas_vendidos}
            columns={[
              { key: 'nombre', label: 'Producto' },
              { key: 'total_vendido', label: 'Unidades Vendidas' },
              { key: 'monto_total', label: 'Monto Total', render: r => `$${parseFloat(r.monto_total).toLocaleString()}` },
            ]}
          />
        )}
      </div>
    </div>
  );
}
