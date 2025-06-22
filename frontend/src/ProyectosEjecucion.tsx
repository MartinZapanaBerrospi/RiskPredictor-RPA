import { useEffect, useState } from 'react';

interface Proyecto {
  id: string;
  tipo_proyecto: string;
  duracion_estimacion: string;
  presupuesto_estimado: string;
  numero_recursos: string;
  tecnologias: string;
  complejidad: string;
  experiencia_equipo: string;
  hitos_clave: string;
}

export default function ProyectosEjecucion() {
  const [proyectos, setProyectos] = useState<Proyecto[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [finalizando, setFinalizando] = useState<string | null>(null);
  const [form, setForm] = useState<any>({});
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/proyectos-ejecucion')
      .then(res => res.json())
      .then(setProyectos)
      .catch(() => setError('Error al cargar proyectos en ejecución'));
  }, [success]);

  const handleInput = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>, id: string) => {
    setForm({ ...form, [id]: { ...form[id], [e.target.name]: e.target.value } });
  };

  const handleFinalizar = async (id: string) => {
    setFinalizando(id);
    setError('');
    setSuccess('');
    try {
      const datos = form[id] || {};
      if (!datos.costo_real || !datos.duracion_real || !datos.riesgo_general) {
        setError('Completa todos los campos para finalizar.');
        setFinalizando(null);
        return;
      }
      const res = await fetch(`http://127.0.0.1:8000/proyectos-ejecucion/${id}/finalizar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos),
      });
      if (!res.ok) throw new Error('Error al finalizar proyecto');
      setSuccess('Proyecto finalizado correctamente');
      setForm({ ...form, [id]: {} });
    } catch (err: any) {
      setError(err.message || 'Error desconocido');
    } finally {
      setFinalizando(null);
    }
  };

  return (
    <div style={{maxWidth: 900, margin: '0 auto'}}>
      <h2>Proyectos en Ejecución</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      {success && <div style={{color: 'green'}}>{success}</div>}
      <table style={{width: '100%', borderCollapse: 'collapse', marginTop: 20}}>
        <thead>
          <tr>
            <th>Tipo</th>
            <th>Duración Estimada</th>
            <th>Presupuesto</th>
            <th>Tecnologías</th>
            <th>Complejidad</th>
            <th>Experiencia</th>
            <th>Hitos</th>
            <th>Costo Real</th>
            <th>Duración Real</th>
            <th>Riesgo General</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          {proyectos.length === 0 && (
            <tr><td colSpan={11}>No hay proyectos en ejecución.</td></tr>
          )}
          {proyectos.map((p) => (
            <tr key={p.id}>
              <td>{p.tipo_proyecto}</td>
              <td>{p.duracion_estimacion}</td>
              <td>{p.presupuesto_estimado}</td>
              <td>{p.tecnologias}</td>
              <td>{p.complejidad}</td>
              <td>{p.experiencia_equipo}</td>
              <td>{p.hitos_clave}</td>
              <td>
                <input
                  type="number"
                  name="costo_real"
                  value={form[p.id]?.costo_real || ''}
                  onChange={e => handleInput(e, p.id)}
                  style={{width: 80}}
                />
              </td>
              <td>
                <input
                  type="number"
                  name="duracion_real"
                  value={form[p.id]?.duracion_real || ''}
                  onChange={e => handleInput(e, p.id)}
                  style={{width: 80}}
                />
              </td>
              <td>
                <select
                  name="riesgo_general"
                  value={form[p.id]?.riesgo_general || ''}
                  onChange={e => handleInput(e, p.id)}
                >
                  <option value="">Seleccione</option>
                  <option value="bajo">Bajo</option>
                  <option value="medio">Medio</option>
                  <option value="alto">Alto</option>
                </select>
              </td>
              <td>
                <button
                  onClick={() => handleFinalizar(p.id)}
                  disabled={finalizando === p.id}
                >
                  {finalizando === p.id ? 'Finalizando...' : 'Finalizar'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
