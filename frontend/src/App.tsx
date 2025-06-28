import { useState, useEffect } from 'react';
import './App.css';
import ProyectosEjecucion from './ProyectosEjecucion';
import ModalResultadoRiesgoPrincipal from './ModalResultadoRiesgoPrincipal';

const initialState = {
  tipo_proyecto: '',
  metodologia: '',
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
  metodologia?: string[];
};

function ThemeToggle() {
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light');
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);
  return (
    <button
      className="theme-toggle"
      aria-label="Cambiar tema"
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
      title={theme === 'light' ? 'Modo oscuro' : 'Modo claro'}
    >
      <span className="icon" style={{transition: 'transform 0.3s'}}>
        {theme === 'light'
          ? (<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>)
          : (<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>)}
      </span>
    </button>
  );
}

function App() {
  const [form, setForm] = useState<any>(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [opciones, setOpciones] = useState<Opciones>({ tipo_proyecto: [], tecnologias: [], metodologia: [] });
  const [view, setView] = useState<'form' | 'proyectos'>('form');
  const [modalRiesgoOpen, setModalRiesgoOpen] = useState(false);
  const [resultadoRiesgo, setResultadoRiesgo] = useState<any>(null);
  const [formPrediccion, setFormPrediccion] = useState<any>(null);
  const [puedeGuardar, setPuedeGuardar] = useState(false);
  const [retrainStatus, setRetrainStatus] = useState('');

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
    setResultadoRiesgo(null);
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
      setResultadoRiesgo(data);
      setFormPrediccion(form);
      setModalRiesgoOpen(true);
      setPuedeGuardar(true);
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
      setPuedeGuardar(false);
    } catch (err: any) {
      setError(err.message || 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };
  const handleLimpiarCampos = () => {
    setForm(initialState);
    setPuedeGuardar(false);
    setResultadoRiesgo(null);
    setFormPrediccion(null);
  };

  const handleRetrain = async () => {
    setRetrainStatus('Reentrenando...');
    try {
      const res = await fetch('http://127.0.0.1:8000/reentrenar-modelo', { method: 'POST' });
      const data = await res.json();
      setRetrainStatus(data.status === 'ok' ? '¡Reentrenamiento completado!' : 'Error al reentrenar');
    } catch {
      setRetrainStatus('Error de red');
    }
  };

  if (view === 'proyectos') {
    return (
      <>
        <ProyectosEjecucion onBack={() => setView('form')} />
      </>
    );
  }

  return (
    <div className="container">
      <ThemeToggle />
      <h1>Predicción de Riesgos en Proyectos TI</h1>
      <form onSubmit={handleSubmit} className="risk-form">
        <div className="form-group">
          <label>Tipo de Proyecto:
            <select name="tipo_proyecto" value={form.tipo_proyecto} onChange={handleChange} required>
              <option value="">Seleccione...</option>
              {opciones.tipo_proyecto.map((op) => (
                <option key={op} value={op}>{op}</option>
              ))}
            </select>
          </label>
        </div>
        <div className="form-group">
          <label>Metodología:
            <select name="metodologia" value={form.metodologia} onChange={handleChange} required>
              <option value="">Seleccione...</option>
              {opciones.metodologia && opciones.metodologia.map((op) => (
                <option key={op} value={op}>{op}</option>
              ))}
            </select>
          </label>
        </div>
        <div className="form-group">
          <label>Duración Estimada (meses):
            <input name="duracion_estimacion" type="number" min="1" value={form.duracion_estimacion} onChange={handleChange} required />
          </label>
        </div>
        <div className="form-group">
          <label>Presupuesto Estimado:
            <input name="presupuesto_estimado" type="number" min="1" value={form.presupuesto_estimado} onChange={handleChange} required />
          </label>
        </div>
        <div className="form-group">
          <label>Número de Recursos:
            <input name="numero_recursos" type="number" min="1" value={form.numero_recursos} onChange={handleChange} required />
          </label>
        </div>
        <div className="form-group tecnologias-group-wrapper">
          <label>Tecnologías:</label>
          <div className="tecnologias-group">
            {opciones.tecnologias.map((tec) => (
              <label key={tec}>
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
        </div>
        <div className="form-group">
          <label>Complejidad:
            <select name="complejidad" value={form.complejidad} onChange={handleChange} required>
              <option value="baja">Baja</option>
              <option value="media">Media</option>
              <option value="alta">Alta</option>
            </select>
          </label>
        </div>
        <div className="form-group">
          <label>Experiencia del Equipo (años):
            <input name="experiencia_equipo" type="number" min="1" value={form.experiencia_equipo} onChange={handleChange} required />
          </label>
        </div>
        <div className="form-group">
          <label>Número de Hitos Clave:
            <input name="hitos_clave" type="number" min="1" value={form.hitos_clave} onChange={handleChange} required />
          </label>
        </div>
        <div className="buttons-row">
          <button type="submit" disabled={loading}>{loading ? 'Prediciendo...' : 'Predecir Riesgo'}</button>
          <button
            type="button"
            onClick={handleGuardarProyecto}
            disabled={loading || !puedeGuardar}
            style={{marginLeft: 0, opacity: !puedeGuardar ? 0.5 : 1, pointerEvents: !puedeGuardar ? 'none' : 'auto'}}
            title={!puedeGuardar ? 'Primero realice una predicción' : 'Guardar en Ejecución'}
          >
            Guardar en Ejecución
          </button>
          <button
            type="button"
            onClick={handleLimpiarCampos}
            disabled={loading}
            style={{marginLeft: 0}}
            title="Limpiar campos"
          >
            Limpiar
          </button>
        </div>
      </form>
      <button onClick={() => setView('proyectos')} style={{marginTop: 20, marginRight: 10}}>
        Ver Proyectos en Ejecución
      </button>
      <button onClick={handleRetrain} style={{marginTop: 20, marginLeft: 10}}>
        Reentrenar modelo
      </button>
      {retrainStatus && <span style={{marginLeft: 10}}>{retrainStatus}</span>}
      {error && <div className="error">{error}</div>}
      <ModalResultadoRiesgoPrincipal
        open={modalRiesgoOpen}
        onClose={() => setModalRiesgoOpen(false)}
        resultado={resultadoRiesgo}
        proyecto={formPrediccion}
      />
    </div>
  );
}

export default App;
