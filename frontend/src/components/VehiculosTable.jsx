import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_vehiculo', label: 'ID' },
  { key: 'id_tipo_vehiculo', label: 'Tipo' },
  { key: 'marca', label: 'Marca' },
  { key: 'modelo', label: 'Modelo' },
  { key: 'año', label: 'Año' },
  { key: 'placas', label: 'Placas' },
  { 
    key: 'estatus', 
    label: 'Estatus',
    render: (row) => (
      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
        row.estatus === 'disponible' ? 'bg-green-100 text-green-800' : 
        row.estatus === 'en ruta' ? 'bg-blue-100 text-blue-800' :
        row.estatus === 'mantenimiento' ? 'bg-yellow-100 text-yellow-800' :
        'bg-red-100 text-red-800'
      }`}>
        {row.estatus}
      </span>
    )
  },
  { key: 'fecha_registro', label: 'Fecha Registro' },
];

export default function VehiculosTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/vehiculos/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Flota de Vehículos ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nuevo Vehículo
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
