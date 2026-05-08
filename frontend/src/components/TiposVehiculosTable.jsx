import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_tipo_vehiculo', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'capacidad_ton', label: 'Capacidad (Ton)' },
  { key: 'fecha_registro', label: 'Fecha Registro' },
];

export default function TiposVehiculosTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/tipos-vehiculos/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Tipos de Vehículos ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nuevo Tipo
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
