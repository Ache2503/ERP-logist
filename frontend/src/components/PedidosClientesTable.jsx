import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_pedido_cliente', label: 'ID' },
  { key: 'numero_pedido', label: 'Número' },
  { key: 'id_cliente', label: 'Cliente' },
  { key: 'id_empleado', label: 'Empleado' },
  { key: 'id_almacen', label: 'Almacén' },
  { 
    key: 'estatus', 
    label: 'Estatus',
    render: (row) => (
      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
        row.estatus === 'completado' ? 'bg-green-100 text-green-800' : 
        row.estatus === 'pendiente' ? 'bg-yellow-100 text-yellow-800' :
        row.estatus === 'cancelado' ? 'bg-red-100 text-red-800' :
        'bg-gray-100 text-gray-800'
      }`}>
        {row.estatus}
      </span>
    )
  },
  { key: 'fecha_pedido', label: 'Fecha' },
];

export default function PedidosClientesTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/pedidos-clientes/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Listado de Pedidos de Clientes ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nuevo Pedido
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
