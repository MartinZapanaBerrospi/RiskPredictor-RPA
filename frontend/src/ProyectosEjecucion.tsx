import { useEffect, useState } from 'react';
import ModalEditarProyecto from './ModalEditarProyecto';
import ModalResultadoRiesgo from './ModalResultadoRiesgo';

// Iconos SVG inline para CRUD
const IconEdit = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19.5 3 21l1.5-4L16.5 3.5z"/></svg>
);
const IconDelete = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
);
const IconBack = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
);

interface Proyecto {
  id: string;
  tipo_proyecto: string;
  metodologia: string;
  duracion_estimacion: string;
  presupuesto_estimado: string;
  numero_recursos: string;
  tecnologias: string;
  complejidad: string;
  experiencia_equipo: string;
  hitos_clave: string;
}

interface ProyectosEjecucionProps {
  onBack?: () => void;
}

const ThemeToggleProyectos = () => {
  const [theme, setTheme] = useState(() => document.documentElement.getAttribute('data-theme') || 'light');
  useEffect(() => {
    const observer = new MutationObserver(() => {
      setTheme(document.documentElement.getAttribute('data-theme') || 'light');
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    return () => observer.disconnect();
  }, []);
  const handleToggle = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    setTheme(newTheme);
  };
  return (
    <button className="theme-toggle-proyectos" aria-label="Cambiar tema" onClick={handleToggle} title={theme === 'light' ? 'Modo oscuro' : 'Modo claro'}>
      <span className="icon" style={{transition: 'transform 0.3s'}}>
        {theme === 'light'
          ? (<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>)
          : (<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>)}
      </span>
    </button>
  );
};

const ToastSuccess = ({ message, onClose }: { message: string, onClose: () => void }) => (
  <div className="toast-success" role="alert">
    <span className="icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
    </span>
    {message}
    <button style={{marginLeft: '1em', background: 'none', border: 'none', color: 'inherit', fontSize: '1.2em', cursor: 'pointer'}} onClick={onClose} aria-label="Cerrar">×</button>
  </div>
);

// Capitaliza la primera letra y pone el resto en minúscula
const capitalize = (str: string) => str ? str.charAt(0).toUpperCase() + str.slice(1).toLowerCase() : '';

export default function ProyectosEjecucion({ onBack }: ProyectosEjecucionProps) {
  const [proyectos, setProyectos] = useState<Proyecto[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [proyectoEdit, setProyectoEdit] = useState<Proyecto | null>(null);
  const [showToast, setShowToast] = useState(false);
  const [modalRiesgoOpen, setModalRiesgoOpen] = useState(false);
  const [resultadoRiesgo, setResultadoRiesgo] = useState<any>(null);
  const [proyectoRiesgo, setProyectoRiesgo] = useState<any>(null);
  useEffect(() => {
    fetch('http://127.0.0.1:8000/proyectos-ejecucion')
      .then(res => res.json())
      .then(setProyectos)
      .catch(() => setError('Error al cargar proyectos en ejecución'));
  }, [success]);

  useEffect(() => {
    const observer = new MutationObserver(() => {
      // setTheme(document.documentElement.getAttribute('data-theme') || 'light'); // Eliminado porque setTheme ya no existe
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (success) {
      setShowToast(true);
      const timer = setTimeout(() => setShowToast(false), 2500);
      return () => clearTimeout(timer);
    }
  }, [success]);

  // CRUD: Eliminar proyecto
  const handleDelete = async (id: string) => {
    if (!window.confirm('¿Seguro que deseas eliminar este proyecto?')) return;
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const res = await fetch(`http://127.0.0.1:8000/proyectos-ejecucion/${id}`, {
        method: 'DELETE',
      });
      if (!res.ok) throw new Error('Error al eliminar proyecto');
      setSuccess('Proyecto eliminado correctamente');
    } catch (err: any) {
      setError(err.message || 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  // CRUD: Editar proyecto (ahora abre modal)
  const handleEdit = (id: string) => {
    const proyecto = proyectos.find(p => p.id === id) || null;
    setProyectoEdit(proyecto);
    setModalOpen(true);
  };
  const handleSaveEdit = async (proyectoActualizado: Partial<Proyecto>) => {
    if (!proyectoActualizado.id) return;
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const res = await fetch(`http://127.0.0.1:8000/proyectos-ejecucion/${proyectoActualizado.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(proyectoActualizado),
      });
      if (!res.ok) throw new Error('Error al actualizar proyecto');
      setSuccess('Proyecto actualizado correctamente');
      setModalOpen(false);
      setProyectoEdit(null);
    } catch (err: any) {
      setError(err.message || 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  // Predicción de riesgo
  const handlePredecir = async (proyecto: Proyecto) => {
    setResultadoRiesgo(null);
    setProyectoRiesgo(proyecto);
    setModalRiesgoOpen(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...proyecto,
          tecnologias: proyecto.tecnologias,
          duracion_estimacion: Number(proyecto.duracion_estimacion),
          presupuesto_estimado: Number(proyecto.presupuesto_estimado),
          numero_recursos: Number(proyecto.numero_recursos),
          experiencia_equipo: Number(proyecto.experiencia_equipo),
          hitos_clave: Number(proyecto.hitos_clave),
        }),
      });
      if (!res.ok) throw new Error('Error al predecir riesgo');
      const data = await res.json();
      setResultadoRiesgo(data);
    } catch (err) {
      setResultadoRiesgo({ error: 'No se pudo predecir el riesgo.' });
    }
  };

  return (
    <>
      <ThemeToggleProyectos />
      <ModalEditarProyecto
        proyecto={proyectoEdit}
        open={modalOpen}
        onClose={() => { setModalOpen(false); setProyectoEdit(null); }}
        onSave={handleSaveEdit}
      />
      <ModalResultadoRiesgo
        open={modalRiesgoOpen}
        onClose={() => setModalRiesgoOpen(false)}
        resultado={resultadoRiesgo}
        proyecto={proyectoRiesgo}
      />
      <div className="container">
        <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%'}}>
          <h2>Proyectos en Ejecución</h2>
        </div>
        {error && <div style={{color: 'red'}}>{error}</div>}
        {success && <div style={{color: 'green'}}>{success}</div>}
        <div className="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Tipo</th>
                <th>Metodología</th>
                <th>Duración Estimada</th>
                <th>Presupuesto</th>
                <th>Recursos</th>
                <th>Tecnologías</th>
                <th>Complejidad</th>
                <th>Experiencia</th>
                <th>Hitos</th>
                <th>Acción</th>
              </tr>
            </thead>
            <tbody>
              {proyectos.length === 0 && (
                <tr><td colSpan={10}>No hay proyectos en ejecución.</td></tr>
              )}
              {proyectos.map((p) => (
                <tr key={p.id}>
                  <td>{capitalize(p.tipo_proyecto)}</td>
                  <td>{capitalize(p.metodologia)}</td>
                  <td>{p.duracion_estimacion}</td>
                  <td>{p.presupuesto_estimado}</td>
                  <td>{p.numero_recursos}</td>
                  <td>{p.tecnologias.split(',').map(capitalize).join(', ')}</td>
                  <td>{capitalize(p.complejidad)}</td>
                  <td>{p.experiencia_equipo}</td>
                  <td>{p.hitos_clave}</td>
                  <td>
                    <button className="crud-btn" onClick={() => handleEdit(p.id)} disabled={loading} title="Editar"><IconEdit /></button>
                    <button className="crud-btn delete" onClick={() => handleDelete(p.id)} disabled={loading} title="Eliminar"><IconDelete /></button>
                    <button className="crud-btn save" onClick={() => handlePredecir(p)} disabled={loading} title="Predecir"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 19V6M5 12l7-7 7 7"/></svg></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="btn-volver">
          <button onClick={onBack || (() => window.history.back())} title="Volver">
            <IconBack /> Volver
          </button>
        </div>
      </div>
      {showToast && <ToastSuccess message={success} onClose={() => setShowToast(false)} />}
    </>
  );
}
