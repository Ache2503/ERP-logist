import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_logistica', label: 'ID' },
  { key: 'id_pedido_cliente', label: 'Pedido' },
  { key: 'id_vehiculo', label: 'Vehículo' },
  { key: 'id_empleado', label: 'Conductor' },
  { 
    key: 'estatus', 
    label: 'Estatus',
    render: (row) => (
      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
        row.estatus === 'entregado' ? 'bg-green-100 text-green-800' : 
        row.estatus === 'en tránsito' ? 'bg-blue-100 text-blue-800' :
        row.estatus === 'pendiente' ? 'bg-yellow-100 text-yellow-800' :
        'bg-gray-100 text-gray-800'
      }`}>
        {row.estatus}
      </span>
    )
  },
  { key: 'fecha_envio', label: 'Fecha Envío' },
  { key: 'fecha_entrega', label: 'Fecha Entrega' },
];

export default function LogisticaTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/logistica/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Gestión de Logística ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nuevo Envío
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
