import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_pedido_cliente', label: 'ID' },
  { key: 'id_cliente', label: 'Cliente ID' },
  { key: 'id_empleado', label: 'Vendedor ID' },
  { key: 'id_almacen', label: 'Almacén' },
  { key: 'fecha', label: 'Fecha' },
  { key: 'subtotal', label: 'Subtotal', render: (row) => `$${parseFloat(row.subtotal || 0).toFixed(2)}` },
  { key: 'impuesto', label: 'Impuesto', render: (row) => `$${parseFloat(row.impuesto || 0).toFixed(2)}` },
  { key: 'total', label: 'Total', render: (row) => `$${parseFloat(row.total || 0).toFixed(2)}` },
  {
    key: 'estatus',
    label: 'Estatus',
    render: (row) => (
      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
        row.estatus === 'completado' || row.estatus === 'entregado' ? 'bg-green-100 text-green-800' :
        row.estatus === 'pendiente' ? 'bg-yellow-100 text-yellow-800' :
        'bg-gray-100 text-gray-800'
      }`}>
        {row.estatus || 'pendiente'}
      </span>
    )
  },
];

export default function VentasTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/ventas');

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
