import React, { useState } from 'react';

interface ModalFinalizarProyectoProps {
  open: boolean;
  onClose: () => void;
  onSave: (data: { costo_real: string; duracion_real: string; riesgo_general: string }) => Promise<void> | void;
  loading?: boolean;
}

const opcionesRiesgo = [
  { value: 'Bajo', label: 'Bajo' },
  { value: 'Medio', label: 'Medio' },
  { value: 'Alto', label: 'Alto' },
];

const ModalFinalizarProyecto: React.FC<ModalFinalizarProyectoProps> = ({ open, onClose, onSave, loading }) => {
  const [form, setForm] = useState({ costo_real: '', duracion_real: '', riesgo_general: 'Bajo' });
  const [error, setError] = useState('');

  React.useEffect(() => {
    if (!open) setForm({ costo_real: '', duracion_real: '', riesgo_general: 'Bajo' });
  }, [open]);

  if (!open) return null;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.costo_real || !form.duracion_real) {
      setError('Completa todos los campos.');
      return;
    }
    setError('');
    await onSave(form);
  };

  return (
    <div className="modal-editar-proyecto-overlay">
      <div className="modal-editar-proyecto finalizar-proyecto">
        <h3>Finalizar Proyecto</h3>
        <form onSubmit={handleSubmit}>
          <label>
            Costo Real (USD):
            <input name="costo_real" type="number" min="0" value={form.costo_real} onChange={handleChange} required disabled={loading} />
          </label>
          <label>
            Duración Real (meses):
            <input name="duracion_real" type="number" min="0" value={form.duracion_real} onChange={handleChange} required disabled={loading} />
          </label>
          <label>
            Riesgo General:
            <select name="riesgo_general" value={form.riesgo_general} onChange={handleChange} required disabled={loading}>
              {opcionesRiesgo.map(op => (
                <option key={op.value} value={op.value}>{op.label}</option>
              ))}
            </select>
          </label>
          {error && <div className="form-error">{error}</div>}
          <div className="modal-editar-proyecto-actions">
            <button type="submit" disabled={loading}>{loading ? 'Guardando...' : 'Guardar'}</button>
            <button type="button" onClick={onClose} className="cancel" disabled={loading}>Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ModalFinalizarProyecto;
