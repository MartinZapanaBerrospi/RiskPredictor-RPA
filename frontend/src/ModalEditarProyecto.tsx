import React, { useEffect, useState } from 'react';

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

interface ModalEditarProyectoProps {
  proyecto: Proyecto | null;
  open: boolean;
  onClose: () => void;
  onSave: (proyecto: Partial<Proyecto>) => void;
}

const opcionesDefault = {
  tipo_proyecto: [],
  tecnologias: [],
  metodologia: [],
};

const ModalEditarProyecto: React.FC<ModalEditarProyectoProps> = ({ proyecto, open, onClose, onSave }) => {
  const [form, setForm] = useState<Partial<Proyecto>>(proyecto || {});
  const [opciones, setOpciones] = useState<any>(opcionesDefault);

  useEffect(() => {
    setForm(proyecto || {});
  }, [proyecto]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/opciones-formulario')
      .then(res => res.json())
      .then(setOpciones)
      .catch(() => setOpciones(opcionesDefault));
  }, []);

  if (!open || !proyecto) return null;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, checked } = e.target as HTMLInputElement;
    if (name === 'tecnologias') {
      let tecs = (form.tecnologias || '').split(',').filter(Boolean);
      if (checked) {
        tecs = [...tecs, value];
      } else {
        tecs = tecs.filter((t) => t !== value);
      }
      setForm({ ...form, tecnologias: tecs.join(',') });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(form);
  };

  const tecsSeleccionadas = (form.tecnologias || '').split(',').filter(Boolean);

  return (
    <div className="modal-editar-proyecto-overlay">
      <div className="modal-editar-proyecto">
        <h3>Editar Proyecto</h3>
        <form onSubmit={handleSubmit}>
          <label>
            Tipo de Proyecto:
            <select name="tipo_proyecto" value={form.tipo_proyecto || ''} onChange={handleChange} required style={{ textTransform: 'capitalize', fontFamily: 'inherit' }}>
              <option value="">Seleccione...</option>
              {opciones.tipo_proyecto.map((op: string) => (
                <option key={op} value={op} style={{ textTransform: 'capitalize', fontFamily: 'inherit' }}>{op}</option>
              ))}
            </select>
          </label>
          <label>
            Metodología:
            <select name="metodologia" value={form.metodologia || ''} onChange={handleChange} required style={{ textTransform: 'capitalize', fontFamily: 'inherit' }}>
              <option value="">Seleccione...</option>
              {opciones.metodologia && opciones.metodologia.map((op: string) => (
                <option key={op} value={op} style={{ textTransform: 'capitalize', fontFamily: 'inherit' }}>{op}</option>
              ))}
            </select>
          </label>
          <label>
            Duración Estimada (meses):
            <input name="duracion_estimacion" type="number" min="1" value={form.duracion_estimacion || ''} onChange={handleChange} required />
          </label>
          <label>
            Presupuesto Estimado:
            <input name="presupuesto_estimado" type="number" min="1" value={form.presupuesto_estimado || ''} onChange={handleChange} required />
          </label>
          <label>
            Número de Recursos:
            <input name="numero_recursos" type="number" min="1" value={form.numero_recursos || ''} onChange={handleChange} required />
          </label>
          <label>
            Tecnologías:
            <div className="tecnologias-group">
              {opciones.tecnologias.map((tec: string) => (
                <label key={tec} style={{fontWeight: 400, textTransform: 'capitalize', fontFamily: 'inherit'}}>
                  <input
                    type="checkbox"
                    name="tecnologias"
                    value={tec}
                    checked={tecsSeleccionadas.includes(tec)}
                    onChange={handleChange}
                  />
                  {tec}
                </label>
              ))}
            </div>
          </label>
          <label>
            Complejidad:
            <select name="complejidad" value={form.complejidad || ''} onChange={handleChange} required>
              <option value="baja">Baja</option>
              <option value="media">Media</option>
              <option value="alta">Alta</option>
            </select>
          </label>
          <label>
            Experiencia del Equipo (años):
            <input name="experiencia_equipo" type="number" min="1" value={form.experiencia_equipo || ''} onChange={handleChange} required />
          </label>
          <label>
            Número de Hitos Clave:
            <input name="hitos_clave" type="number" min="1" value={form.hitos_clave || ''} onChange={handleChange} required />
          </label>
          <div className="modal-editar-proyecto-actions">
            <button type="submit">Guardar</button>
            <button type="button" onClick={onClose} className="cancel">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ModalEditarProyecto;
