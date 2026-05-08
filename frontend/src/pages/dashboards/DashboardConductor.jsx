import { useState, useEffect, useCallback } from 'react';
import { getAuthHeaders } from '../../hooks/useApi';
import { useAuth } from '../../hooks/useAuth';
import API_BASE from '../../config';

const API = API_BASE;

export default function DashboardConductor() {
  const { empleado } = useAuth();
  const id = empleado?.id_empleado;

  const [tab, setTab] = useState('envios');
  const [stats, setStats] = useState(null);
  const [envios, setEnvios] = useState({ total: 0, data: [] });
  const [incidentes, setIncidentes] = useState({ total: 0, data: [] });
  const [resenas, setResenas] = useState([]);
  const [perfil, setPerfil] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [showIncidenteModal, setShowIncidenteModal] = useState(false);
  const [incidenteForm, setIncidenteForm] = useState({ tipo: 'otro', descripcion: '', id_envio: '' });
  const [incidenteSubmitting, setIncidenteSubmitting] = useState(false);

  const [editPerfil, setEditPerfil] = useState(false);
  const [perfilForm, setPerfilForm] = useState({ telefono: '', direccion: '', email: '' });

  const [detalleEnvio, setDetalleEnvio] = useState(null);
  const [loadingDetalle, setLoadingDetalle] = useState(false);

  const safeDate = (d) => {
    if (!d) return '';
    const ds = d.includes('T') ? d + 'Z' : d + 'T00:00:00Z';
    const dt = new Date(ds);
    return isNaN(dt.getTime()) ? d : dt.toLocaleDateString();
  };

  const fetchData = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    setError('');
    const h = getAuthHeaders();
    const [sRes, eRes, iRes, rRes, pRes] = await Promise.all([
      fetch(`${API}/conductores/${id}/dashboard/estadisticas`, { headers: h }),
      fetch(`${API}/conductores/${id}/dashboard/envios?skip=0&limit=50`, { headers: h }),
      fetch(`${API}/conductores/${id}/dashboard/incidentes?skip=0&limit=50`, { headers: h }),
      fetch(`${API}/conductores/${id}/dashboard/resenas?skip=0&limit=50`, { headers: h }),
      fetch(`${API}/conductores/${id}/dashboard/perfil`, { headers: h }),
    ]);
    if (sRes.ok) setStats(await sRes.json());
    if (eRes.ok) setEnvios(await eRes.json());
    if (iRes.ok) setIncidentes(await iRes.json());
    if (rRes.ok) setResenas(await rRes.json());
    if (pRes.ok) {
      const p = await pRes.json();
      setPerfil(p);
      setPerfilForm({ telefono: p.telefono || '', direccion: p.direccion || '', email: p.email || '' });
    }
    if (!sRes.ok || !eRes.ok) setError('Error al cargar datos del dashboard');
    setLoading(false);
  }, [id]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const verDetalleEnvio = async (idEnvio) => {
    setLoadingDetalle(true);
    setDetalleEnvio(null);
    try {
      const res = await fetch(`${API}/conductores/${id}/dashboard/envios/${idEnvio}`, { headers: getAuthHeaders() });
      if (!res.ok) throw new Error('Error al cargar detalle');
      setDetalleEnvio(await res.json());
    } catch (err) {
      alert(err.message);
    } finally {
      setLoadingDetalle(false);
    }
  };

  const actualizarEstatusEnvio = async (idEnvio, estatus) => {
    if (!window.confirm(`¿Marcar envío #${idEnvio} como "${estatus}"?`)) return;
    try {
      const res = await fetch(`${API}/conductores/${id}/dashboard/envios/${idEnvio}/estatus?estatus=${estatus}`, {
        method: 'POST',
        headers: getAuthHeaders(),
      });
      if (!res.ok) throw new Error('Error al actualizar estatus');
      alert('Estatus actualizado');
      fetchData();
      setDetalleEnvio(null);
    } catch (err) {
      alert(err.message);
    }
  };

  const reportarIncidente = async (e) => {
    e.preventDefault();
    if (!incidenteForm.descripcion.trim()) return alert('Describe el incidente');
    if (!incidenteForm.id_envio) return alert('Selecciona un envío');
    setIncidenteSubmitting(true);
    try {
      const res = await fetch(`${API}/conductores/${id}/dashboard/incidentes`, {
        method: 'POST',
        headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tipo: incidenteForm.tipo,
          descripcion: incidenteForm.descripcion,
          id_envio: parseInt(incidenteForm.id_envio),
        }),
      });
      if (!res.ok) throw new Error('Error al reportar incidente');
      setShowIncidenteModal(false);
      setIncidenteForm({ tipo: 'otro', descripcion: '', id_envio: '' });
      fetchData();
      alert('Incidente reportado');
    } catch (err) {
      alert(err.message);
    } finally {
      setIncidenteSubmitting(false);
    }
  };

  const guardarPerfil = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API}/conductores/${id}/dashboard/perfil`, {
        method: 'PUT',
        headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' },
        body: JSON.stringify(perfilForm),
      });
      if (!res.ok) throw new Error('Error al actualizar perfil');
      setPerfil(await res.json());
      setEditPerfil(false);
      alert('Perfil actualizado');
    } catch (err) {
      alert(err.message);
    }
  };

  const estatusColor = (est) => {
    const map = {
      pendiente: 'bg-yellow-100 text-yellow-800',
      en_ruta: 'bg-blue-100 text-blue-800',
      entregado: 'bg-green-100 text-green-800',
      fallido: 'bg-red-100 text-red-800',
      cancelado: 'bg-gray-100 text-gray-800',
    };
    return map[est] || 'bg-gray-100 text-gray-800';
  };

  const renderStars = (cal) => {
    const full = Math.floor(cal);
    const half = cal % 1 >= 0.5;
    const stars = [];
    for (let i = 0; i < 5; i++) {
      if (i < full) stars.push('★');
      else if (i === full && half) stars.push('⯪');
      else stars.push('☆');
    }
    return <span className="text-yellow-500 text-lg">{stars.join('')}</span>;
  };

  if (loading) return <p className="p-6 text-gray-500">Cargando panel...</p>;
  if (error) return <div className="p-6 bg-red-50 border border-red-200 text-red-700 rounded-lg">{error}</div>;

  const enviosPendientes = stats?.pendientes ?? envios.data.filter(e => e.estatus_envio === 'pendiente').length;
  const enviosEnRuta = stats?.en_ruta ?? envios.data.filter(e => e.estatus_envio === 'en_ruta').length;
  const enviosEntregados = stats?.entregados ?? envios.data.filter(e => e.estatus_envio === 'entregado').length;

  const tabs = [
    { key: 'envios', label: `Mis Envíos (${envios.total})` },
    { key: 'incidentes', label: `Incidentes (${incidentes.total})` },
    { key: 'resenas', label: `Reseñas (${resenas.length})` },
    { key: 'perfil', label: 'Mi Perfil' },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold">Panel del Transportista</h2>
          <p className="text-gray-600">Bienvenido, {empleado?.nombre} {empleado?.apellido}</p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow border-l-4 border-yellow-500">
          <p className="text-xs text-gray-500 uppercase tracking-wide">Pendientes</p>
          <p className="text-3xl font-bold">{enviosPendientes}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow border-l-4 border-blue-500">
          <p className="text-xs text-gray-500 uppercase tracking-wide">En Ruta</p>
          <p className="text-3xl font-bold">{enviosEnRuta}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow border-l-4 border-green-500">
          <p className="text-xs text-gray-500 uppercase tracking-wide">Entregados</p>
          <p className="text-3xl font-bold">{enviosEntregados}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow border-l-4 border-purple-500">
          <p className="text-xs text-gray-500 uppercase tracking-wide">Calificación</p>
          <p className="text-3xl font-bold">
            {stats?.calificacion_promedio ? stats.calificacion_promedio.toFixed(1) : '—'}
          </p>
          {stats?.total_resenas > 0 && (
            <p className="text-xs text-gray-400">{stats.total_resenas} reseña(s)</p>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-4 border-b">
        {tabs.map(t => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-4 py-2 text-sm font-medium rounded-t transition-colors ${
              tab === t.key ? 'bg-white border-l border-r border-t -mb-px text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab: Envíos */}
      {tab === 'envios' && (
        <div>
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-semibold text-lg">Envíos Asignados</h3>
          </div>
          {envios.data.length === 0 ? (
            <div className="bg-white p-8 rounded-lg shadow text-center text-gray-500">
              No tienes envíos asignados actualmente.
            </div>
          ) : (
            <div className="space-y-3">
              {envios.data.map(env => (
                <div key={env.id_asignacion || env.id_envio} className="bg-white p-4 rounded-lg shadow">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">
                        Pedido #{env.id_pedido_cliente} — {env.cliente_nombre || 'Cliente'}
                      </p>
                      <p className="text-sm text-gray-500">
                        Envío #{env.id_envio}
                        {env.total_pedido != null && ` | $${Number(env.total_pedido).toFixed(2)}`}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${estatusColor(env.estatus_envio)}`}>
                        {env.estatus_envio || 'pendiente'}
                      </span>
                      <button
                        onClick={() => verDetalleEnvio(env.id_envio)}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        Detalle
                      </button>
                    </div>
                  </div>

                  {/* Acciones rápidas por estatus */}
                  <div className="mt-3 flex gap-2">
                    {env.estatus_envio === 'pendiente' && (
                      <button onClick={() => actualizarEstatusEnvio(env.id_envio, 'en_ruta')}
                        className="bg-blue-600 text-white px-3 py-1 rounded text-xs hover:bg-blue-700">
                        Iniciar Ruta
                      </button>
                    )}
                    {env.estatus_envio === 'en_ruta' && (
                      <>
                        <button onClick={() => actualizarEstatusEnvio(env.id_envio, 'entregado')}
                          className="bg-green-600 text-white px-3 py-1 rounded text-xs hover:bg-green-700">
                          Marcar Entregado
                        </button>
                        <button onClick={() => actualizarEstatusEnvio(env.id_envio, 'fallido')}
                          className="bg-red-600 text-white px-3 py-1 rounded text-xs hover:bg-red-700">
                          Marcar Fallido
                        </button>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Detalle de envío */}
          {detalleEnvio && (
            <div className="mt-6 bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-lg">Detalle Envío #{detalleEnvio.id_envio}</h3>
                <button onClick={() => setDetalleEnvio(null)} className="text-gray-400 hover:text-gray-600 text-xl">&times;</button>
              </div>
              {loadingDetalle ? (
                <p className="text-gray-500">Cargando detalle...</p>
              ) : (
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium text-sm text-gray-500 uppercase mb-2">Información</h4>
                    <p><span className="text-gray-500">Estatus:</span> {detalleEnvio.estatus}</p>
                    <p><span className="text-gray-500">Fecha:</span> {detalleEnvio.fecha_envio}</p>
                    <p><span className="text-gray-500">Vehículo:</span> {detalleEnvio.vehiculo?.placa || '—'}</p>
                    {detalleEnvio.cliente && (
                      <>
                        <p><span className="text-gray-500">Cliente:</span> {detalleEnvio.cliente.nombre} {detalleEnvio.cliente.apellido}</p>
                        <p><span className="text-gray-500">Dirección:</span> {detalleEnvio.cliente.direccion || '—'}</p>
                      </>
                    )}
                  </div>
                  <div>
                    <h4 className="font-medium text-sm text-gray-500 uppercase mb-2">Productos</h4>
                    {detalleEnvio.productos?.length > 0 ? (
                      <ul className="divide-y">
                        {detalleEnvio.productos.map((p, i) => (
                          <li key={i} className="py-1 flex justify-between">
                            <span>{p.nombre_producto || p.producto}</span>
                            <span className="text-gray-500">x{p.cantidad}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-gray-400">Sin productos</p>
                    )}
                  </div>
                  <div className="md:col-span-2">
                    <h4 className="font-medium text-sm text-gray-500 uppercase mb-2">Seguimiento</h4>
                    {detalleEnvio.seguimiento?.length > 0 ? (
                      <div className="space-y-3">
                        {detalleEnvio.seguimiento.map((s, i) => (
                          <div key={i} className="flex gap-3">
                            <div className="flex flex-col items-center">
                              <div className={`w-3 h-3 rounded-full ${i === 0 ? 'bg-blue-500' : 'bg-gray-300'}`} />
                              {i < detalleEnvio.seguimiento.length - 1 && <div className="w-0.5 h-8 bg-gray-200" />}
                            </div>
                            <div>
                              <p className="text-sm font-medium">{s.estatus_nuevo}</p>
                              <p className="text-xs text-gray-500">{s.fecha_cambio} {s.hora_cambio && `- ${s.hora_cambio}`}</p>
                              {s.ubicacion && <p className="text-xs text-gray-400">{s.ubicacion}</p>}
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-gray-400">Sin seguimiento registrado</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Tab: Incidentes */}
      {tab === 'incidentes' && (
        <div>
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-semibold text-lg">Incidentes Reportados</h3>
            <button onClick={() => setShowIncidenteModal(true)}
              className="bg-red-600 text-white px-4 py-2 rounded text-sm hover:bg-red-700">
              + Reportar Incidente
            </button>
          </div>
          {incidentes.data.length === 0 ? (
            <div className="bg-white p-8 rounded-lg shadow text-center text-gray-500">
              No has reportado incidentes.
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow divide-y">
              {incidentes.data.map((inc, i) => (
                <div key={inc.id_incidente || i} className="p-4">
                  <div className="flex items-center justify-between mb-1">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                      inc.tipo === 'accidente' ? 'bg-red-100 text-red-800' :
                      inc.tipo === 'retraso' ? 'bg-yellow-100 text-yellow-800' :
                      inc.tipo === 'averia' ? 'bg-orange-100 text-orange-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>{inc.tipo}</span>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                      inc.estatus === 'pendiente' ? 'bg-yellow-100 text-yellow-800' :
                      inc.estatus === 'en_revision' ? 'bg-blue-100 text-blue-800' :
                      inc.estatus === 'resuelto' ? 'bg-green-100 text-green-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>{inc.estatus || 'pendiente'}</span>
                  </div>
                  <p className="text-sm text-gray-700 mb-1">{inc.descripcion}</p>
                  <p className="text-xs text-gray-400">
                    Envío #{inc.id_envio} | {safeDate(inc.fecha_reporte)}
                  </p>
                </div>
              ))}
            </div>
          )}

          {/* Modal Incidente */}
          {showIncidenteModal && (
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
                <h3 className="text-lg font-bold mb-4">Reportar Incidente</h3>
                <form onSubmit={reportarIncidente}>
                  <div className="mb-3">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
                    <select value={incidenteForm.tipo} onChange={e => setIncidenteForm(f => ({ ...f, tipo: e.target.value }))}
                      className="w-full border rounded px-3 py-2 text-sm">
                      <option value="accidente">Accidente</option>
                      <option value="retraso">Retraso</option>
                      <option value="averia">Avería</option>
                      <option value="otro">Otro</option>
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Envío</label>
                    <select value={incidenteForm.id_envio} onChange={e => setIncidenteForm(f => ({ ...f, id_envio: e.target.value }))}
                      className="w-full border rounded px-3 py-2 text-sm">
                      <option value="">Seleccionar envío...</option>
                      {envios.data.map(env => (
                        <option key={env.id_envio} value={env.id_envio}>
                          #{env.id_envio} - Pedido {env.id_pedido_cliente} ({env.cliente_nombre || '—'})
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
                    <textarea value={incidenteForm.descripcion} onChange={e => setIncidenteForm(f => ({ ...f, descripcion: e.target.value }))}
                      className="w-full border rounded px-3 py-2 text-sm" rows={3} required />
                  </div>
                  <div className="flex justify-end gap-2">
                    <button type="button" onClick={() => setShowIncidenteModal(false)}
                      className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800">Cancelar</button>
                    <button type="submit" disabled={incidenteSubmitting}
                      className="bg-red-600 text-white px-4 py-2 rounded text-sm hover:bg-red-700 disabled:opacity-50">
                      {incidenteSubmitting ? 'Enviando...' : 'Reportar'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab: Reseñas */}
      {tab === 'resenas' && (
        <div>
          <h3 className="font-semibold text-lg mb-3">Reseñas de Clientes</h3>
          {resenas.length === 0 ? (
            <div className="bg-white p-8 rounded-lg shadow text-center text-gray-500">
              Aún no tienes reseñas.
            </div>
          ) : (
            <div className="space-y-3">
              {resenas.map((r, i) => (
                <div key={r.id_resena || i} className="bg-white p-4 rounded-lg shadow">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {renderStars(r.calificacion)}
                      <span className="text-sm font-medium">{r.cliente_nombre || 'Cliente'}</span>
                    </div>
                    <span className="text-xs text-gray-400">
                      {safeDate(r.fecha_resena)}
                    </span>
                  </div>
                  {r.comentario && <p className="text-sm text-gray-700">{r.comentario}</p>}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Tab: Perfil */}
      {tab === 'perfil' && (
        <div>
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-semibold text-lg">Mi Perfil</h3>
            {!editPerfil && (
              <button onClick={() => setEditPerfil(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">
                Editar Perfil
              </button>
            )}
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            {!editPerfil ? (
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Nombre</p>
                  <p className="font-medium">{perfil?.nombre} {perfil?.apellido}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Email</p>
                  <p className="font-medium">{perfil?.email || '—'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Teléfono</p>
                  <p className="font-medium">{perfil?.telefono || '—'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Dirección</p>
                  <p className="font-medium">{perfil?.direccion || '—'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Cargo</p>
                  <p className="font-medium">{perfil?.cargo || '—'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Licencia</p>
                  <p className="font-medium">{perfil?.licencia_conducir || '—'}</p>
                </div>
              </div>
            ) : (
              <form onSubmit={guardarPerfil} className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input type="email" value={perfilForm.email}
                    onChange={e => setPerfilForm(f => ({ ...f, email: e.target.value }))}
                    className="w-full border rounded px-3 py-2 text-sm" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
                  <input type="text" value={perfilForm.telefono}
                    onChange={e => setPerfilForm(f => ({ ...f, telefono: e.target.value }))}
                    className="w-full border rounded px-3 py-2 text-sm" />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
                  <input type="text" value={perfilForm.direccion}
                    onChange={e => setPerfilForm(f => ({ ...f, direccion: e.target.value }))}
                    className="w-full border rounded px-3 py-2 text-sm" />
                </div>
                <div className="md:col-span-2 flex justify-end gap-2">
                  <button type="button" onClick={() => setEditPerfil(false)}
                    className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800">Cancelar</button>
                  <button type="submit"
                    className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">Guardar</button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
