import { useState, useEffect } from 'react';
import './App.css';
import ProyectosEjecucion from './ProyectosEjecucion';

const initialState = {
  tipo_proyecto: '',
  duracion_estimacion: '',
  presupuesto_estimado: '',
  numero_recursos: '',
  tecnologias: [],
  complejidad: 'media',
  experiencia_equipo: '',
  hitos_clave: '',
};

type Opciones = {
  tipo_proyecto: string[];
  tecnologias: string[];
};

function App() {
  const [form, setForm] = useState<any>(initialState);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [opciones, setOpciones] = useState<Opciones>({ tipo_proyecto: [], tecnologias: [] });
  const [retrainStatus, setRetrainStatus] = useState<'idle' | 'loading' | 'ok' | 'error'>('idle');
  const [retrainOutput, setRetrainOutput] = useState<string>('');
  const [view, setView] = useState<'form' | 'proyectos'>('form');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/opciones-formulario')
      .then(res => res.json())
      .then(setOpciones);
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, checked } = e.target as HTMLInputElement;
    if (name === 'tecnologias') {
      if (checked) {
        setForm({ ...form, tecnologias: [...form.tecnologias, value] });
      } else {
        setForm({ ...form, tecnologias: form.tecnologias.filter((t: string) => t !== value) });
      }
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          tecnologias: form.tecnologias.join(','),
          duracion_estimacion: Number(form.duracion_estimacion),
          presupuesto_estimado: Number(form.presupuesto_estimado),
          numero_recursos: Number(form.numero_recursos),
          experiencia_equipo: Number(form.experiencia_equipo),
          hitos_clave: Number(form.hitos_clave),
        }),
      });
      if (!response.ok) throw new Error('Error en la predicción');
      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  // Nuevo: Guardar proyecto en ejecución
  const handleGuardarProyecto = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://127.0.0.1:8000/proyectos-ejecucion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          tecnologias: form.tecnologias.join(','),
          duracion_estimacion: Number(form.duracion_estimacion),
          presupuesto_estimado: Number(form.presupuesto_estimado),
          numero_recursos: Number(form.numero_recursos),
          experiencia_equipo: Number(form.experiencia_equipo),
          hitos_clave: Number(form.hitos_clave),
        }),
      });
      if (!response.ok) throw new Error('Error al guardar el proyecto');
      alert('Proyecto guardado en ejecución');
      setForm(initialState);
    } catch (err: any) {
      setError(err.message || 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  // Reentrenar modelo
  const handleRetrain = async () => {
    setRetrainStatus('loading');
    setRetrainOutput('');
    try {
      const response = await fetch('http://127.0.0.1:8000/reentrenar-modelo', {
        method: 'POST',
      });
      const data = await response.json();
      if (data.status === 'ok') {
        setRetrainStatus('ok');
        setRetrainOutput(data.output);
      } else {
        setRetrainStatus('error');
        setRetrainOutput(data.output || 'Error desconocido');
      }
    } catch (err: any) {
      setRetrainStatus('error');
      setRetrainOutput(err.message || 'Error desconocido');
    }
  };

  if (view === 'proyectos') {
    return (
      <div className="container">
        <button onClick={() => setView('form')} style={{marginBottom: 20}}>Volver</button>
        <ProyectosEjecucion />
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Predicción de Riesgos en Proyectos TI</h1>
      <form onSubmit={handleSubmit} className="risk-form">
        <label>Tipo de Proyecto:
          <select name="tipo_proyecto" value={form.tipo_proyecto} onChange={handleChange} required>
            <option value="">Seleccione...</option>
            {opciones.tipo_proyecto.map((op) => (
              <option key={op} value={op}>{op}</option>
            ))}
          </select>
        </label>
        <label>Duración Estimada (meses):
          <input name="duracion_estimacion" type="number" min="1" value={form.duracion_estimacion} onChange={handleChange} required />
        </label>
        <label>Presupuesto Estimado:
          <input name="presupuesto_estimado" type="number" min="1" value={form.presupuesto_estimado} onChange={handleChange} required />
        </label>
        <label>Número de Recursos:
          <input name="numero_recursos" type="number" min="1" value={form.numero_recursos} onChange={handleChange} required />
        </label>
        <label>Tecnologías:</label>
        <div className="tecnologias-group">
          {opciones.tecnologias.map((tec) => (
            <label key={tec} style={{marginRight: 10}}>
              <input
                type="checkbox"
                name="tecnologias"
                value={tec}
                checked={form.tecnologias.includes(tec)}
                onChange={handleChange}
              />
              {tec}
            </label>
          ))}
        </div>
        <label>Complejidad:
          <select name="complejidad" value={form.complejidad} onChange={handleChange} required>
            <option value="baja">Baja</option>
            <option value="media">Media</option>
            <option value="alta">Alta</option>
          </select>
        </label>
        <label>Experiencia del Equipo (años):
          <input name="experiencia_equipo" type="number" min="1" value={form.experiencia_equipo} onChange={handleChange} required />
        </label>
        <label>Número de Hitos Clave:
          <input name="hitos_clave" type="number" min="1" value={form.hitos_clave} onChange={handleChange} required />
        </label>
        <button type="submit" disabled={loading}>{loading ? 'Prediciendo...' : 'Predecir Riesgo'}</button>
        <button type="button" onClick={handleGuardarProyecto} disabled={loading} style={{marginLeft: 10}}>
          Guardar en Ejecución
        </button>
      </form>
      <button onClick={() => setView('proyectos')} style={{marginTop: 20, marginRight: 10}}>
        Ver Proyectos en Ejecución
      </button>
      <button onClick={handleRetrain} disabled={retrainStatus === 'loading'} style={{marginTop: 20}}>
        {retrainStatus === 'loading' ? 'Reentrenando...' : 'Reentrenar Modelo'}
      </button>
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result">
          <h2>Resultado</h2>
          <p><b>Riesgo General:</b> {result.riesgo_general}</p>
          <p><b>Probabilidades de Riesgo:</b></p>
          <ul>
            {Object.entries(result.probabilidades_riesgo).map(([k, v]) => (
              <li key={k}>{k}: {(v as number * 100).toFixed(1)}%</li>
            ))}
          </ul>
          <p><b>Probabilidad de Sobrecosto:</b> {(result.probabilidad_sobrecosto * 100).toFixed(1)}%</p>
          <p><b>Probabilidad de Retraso:</b> {(result.probabilidad_retraso * 100).toFixed(1)}%</p>
        </div>
      )}
      {retrainStatus !== 'idle' && (
        <div className="retrain-status" style={{marginTop: 10}}>
          <b>Estado de reentrenamiento:</b> {retrainStatus === 'ok' ? '¡Completado!' : retrainStatus === 'loading' ? 'En progreso...' : 'Error'}
          <pre style={{background: '#f4f4f4', padding: 10, maxHeight: 200, overflow: 'auto'}}>{retrainOutput}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
