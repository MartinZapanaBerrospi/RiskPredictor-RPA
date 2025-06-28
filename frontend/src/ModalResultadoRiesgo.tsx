import React from 'react';
import ReportePDFButton from './ReportePDFButton';

interface ResultadoRiesgo {
  riesgo_general: string;
  probabilidades_riesgo: Record<string, number>;
  probabilidad_sobrecosto: number;
  probabilidad_retraso: number;
}

interface ModalResultadoRiesgoProps {
  open: boolean;
  onClose: () => void;
  resultado: ResultadoRiesgo | null;
  proyecto: any;
}

const ModalResultadoRiesgo: React.FC<ModalResultadoRiesgoProps> = ({ open, onClose, resultado, proyecto }) => {
  if (!open || !resultado) return null;
  return (
    <div className="modal-editar-proyecto-overlay">
      <div className="modal-editar-proyecto" style={{maxWidth: 500}}>
        <h3>Resultado de Predicción</h3>
        <div className="result" style={{margin: 0}}>
          <p><b>Riesgo General:</b> {resultado.riesgo_general}</p>
          <p><b>Probabilidades de Riesgo:</b></p>
          <ul>
            {Object.entries(resultado.probabilidades_riesgo).map(([k, v]) => (
              <li key={k}>{k}: {(v * 100).toFixed(1)}%</li>
            ))}
          </ul>
          <p><b>Probabilidad de Sobrecosto:</b> {(resultado.probabilidad_sobrecosto * 100).toFixed(1)}%</p>
          <p><b>Probabilidad de Retraso:</b> {(resultado.probabilidad_retraso * 100).toFixed(1)}%</p>
        </div>
        <div className="modal-editar-proyecto-actions">
          <ReportePDFButton formData={{
            ...proyecto,
            tecnologias: Array.isArray(proyecto.tecnologias)
              ? proyecto.tecnologias
              : (typeof proyecto.tecnologias === 'string' ? proyecto.tecnologias.split(',').map((t: string) => t.trim()) : []),
          }} />
          <button type="button" onClick={onClose} className="cancel">Cerrar</button>
        </div>
      </div>
    </div>
  );
};

export default ModalResultadoRiesgo;
