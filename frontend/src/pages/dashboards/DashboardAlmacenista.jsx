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

export default function DashboardAlmacenista() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/reportes/inventario`, { headers: getAuthHeaders() }).then(r => r.json()),
      fetch(`${API}/almacenes`, { headers: getAuthHeaders() }).then(r => r.json()),
      fetch(`${API}/productos`, { headers: getAuthHeaders() }).then(r => r.json()),
      fetch(`${API}/inventario/bajo-stock`, { headers: getAuthHeaders() }).then(r => r.json()),
    ])
      .then(([inv, almas, prods, bajo]) => {
        setData({
          inventario: inv,
          almacenes: almas.total || (Array.isArray(almas) ? almas.length : 0),
          productos: Array.isArray(prods) ? prods.length : 0,
          bajoStock: Array.isArray(bajo) ? bajo : [],
        });
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <p className="p-6">Cargando...</p>;
  if (!data) return <p className="p-6">Error al cargar datos</p>;

  const { inventario, almacenes, productos, bajoStock } = data;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Panel de Almacén</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card title="Almacenes" value={almacenes} color="border-blue-500" />
        <Card title="Productos" value={productos} color="border-green-500" />
        <Card title="Unidades en Stock" value={inventario?.total_en_stock || 0} color="border-yellow-500" />
        <Card title="Valor Inventario" value={`$${parseFloat(inventario?.valor_total_inventario || 0).toLocaleString()}`} color="border-purple-500" />
      </div>
      {bajoStock.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-red-800 mb-2">⚠ Productos con Stock Bajo ({bajoStock.length})</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead><tr className="border-b border-red-200 text-left"><th className="pb-2 text-red-700">Producto</th><th className="pb-2 text-red-700">Stock Actual</th></tr></thead>
              <tbody>
                {bajoStock.map((item, i) => (
                  <tr key={i} className="border-b border-red-100 last:border-0">
                    <td className="py-2 text-red-700">{item.producto?.nombre || `ID ${item.id_producto}`}</td>
                    <td className="py-2 text-red-700 font-medium">{item.cantidad || 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      {inventario?.productos_bajo_stock > 0 && bajoStock.length === 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-700 font-medium">{inventario.productos_bajo_stock} producto(s) con stock bajo</p>
        </div>
      )}
      <div className="bg-green-50 p-4 rounded-lg">
        <p className="text-green-700 font-medium mb-2">Accesos rápidos:</p>
        <div className="flex gap-2">
          <a href="/almacenes" className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">Almacenes</a>
          <a href="/productos" className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700">Productos</a>
          <a href="/inventario" className="bg-yellow-600 text-white px-4 py-2 rounded text-sm hover:bg-yellow-700">Inventario</a>
        </div>
      </div>
    </div>
  );
}
