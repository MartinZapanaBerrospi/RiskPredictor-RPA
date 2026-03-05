import React, { useState } from 'react';
import ReportePDFButton from './ReportePDFButton';
import ModalEnviarEmail from './ModalEnviarEmail';
import Toast from './Toast';

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

function getRiskColor(level: string): string {
  const l = level.toLowerCase();
  if (l === 'alto') return '#ef4444';
  if (l === 'medio') return '#f59e0b';
  return '#22c55e';
}

function getRiskIcon(level: string): string {
  const l = level.toLowerCase();
  if (l === 'alto') return '🔴';
  if (l === 'medio') return '🟡';
  return '🟢';
}

function getBarColor(value: number): string {
  if (value > 0.6) return '#ef4444';
  if (value > 0.3) return '#f59e0b';
  return '#22c55e';
}

const ModalResultadoRiesgo: React.FC<ModalResultadoRiesgoProps> = ({ open, onClose, resultado, proyecto }) => {
  const [modalEmailOpen, setModalEmailOpen] = useState(false);
  const [loadingEmail, setLoadingEmail] = useState(false);
  const [toast, setToast] = useState<{message: string, type: 'success'|'error'}|null>(null);

  const handleSendEmail = async (email: string) => {
    setLoadingEmail(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/enviar-reporte-mailhog`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          destinatario: email,
          proyecto: {
            ...proyecto,
            tecnologias: Array.isArray(proyecto.tecnologias)
              ? proyecto.tecnologias.join(',')
              : (typeof proyecto.tecnologias === 'string' ? proyecto.tecnologias : ''),
            duracion_estimacion: Number(proyecto.duracion_estimacion),
            presupuesto_estimado: Number(proyecto.presupuesto_estimado),
            numero_recursos: Number(proyecto.numero_recursos),
            experiencia_equipo: Number(proyecto.experiencia_equipo),
            hitos_clave: Number(proyecto.hitos_clave),
          },
          prediccion: resultado
        })
      });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || 'No se pudo enviar el email. Verifica la configuración SMTP en Render.');
      }
      setToast({ message: '✅ Reporte enviado exitosamente', type: 'success' });
      setModalEmailOpen(false);
    } catch (e: any) {
      setToast({ message: e.message || 'Error al enviar email', type: 'error' });
    } finally {
      setLoadingEmail(false);
    }
  };

  if (!open || !resultado) return null;

  const riskColor = getRiskColor(resultado.riesgo_general);
  const riskIcon = getRiskIcon(resultado.riesgo_general);

  return (
    <>
      <div className="modal-editar-proyecto-overlay">
        <div className="modal-resultado-premium">
          
          {/* Header */}
          <div className="modal-resultado-header">
            <div>
              <h3>Resultado de Predicción</h3>
              <p>Motor Analítico — XGBoost</p>
            </div>
            <button className="modal-close-btn" onClick={onClose}>✕</button>
          </div>

          {/* Body */}
          <div className="modal-resultado-body">
            
            {/* Risk Badge */}
            <div className="risk-badge" style={{ 
              borderColor: riskColor,
              color: riskColor,
            }}>
              <span style={{ fontSize: '1.4rem' }}>{riskIcon}</span>
              Riesgo {resultado.riesgo_general}
            </div>

            {/* Probabilidades */}
            <div className="prob-section">
              <p className="prob-label">Distribución de Probabilidades</p>
              {Object.entries(resultado.probabilidades_riesgo).map(([key, value]) => {
                const pct = (value * 100).toFixed(1);
                const barColor = getBarColor(value);
                return (
                  <div key={key} className="prob-row">
                    <div className="prob-row-header">
                      <span className="prob-name">{key}</span>
                      <span className="prob-value" style={{ color: barColor }}>{pct}%</span>
                    </div>
                    <div className="prob-bar-track">
                      <div className="prob-bar-fill" style={{
                        width: `${Math.max(Number(pct), 2)}%`,
                        background: barColor,
                      }} />
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Metric Cards */}
            <div className="metric-cards">
              <div className="metric-card metric-card-rose">
                <span className="metric-label">Sobrecosto</span>
                <span className="metric-value" style={{ color: getBarColor(resultado.probabilidad_sobrecosto) }}>
                  {(resultado.probabilidad_sobrecosto * 100).toFixed(1)}%
                </span>
              </div>
              <div className="metric-card metric-card-amber">
                <span className="metric-label">Retraso</span>
                <span className="metric-value" style={{ color: getBarColor(resultado.probabilidad_retraso) }}>
                  {(resultado.probabilidad_retraso * 100).toFixed(1)}%
                </span>
              </div>
            </div>

            {/* Actions */}
            <div className="modal-resultado-actions">
              <ReportePDFButton formData={{
                ...proyecto,
                tecnologias: Array.isArray(proyecto.tecnologias)
                  ? proyecto.tecnologias
                  : (typeof proyecto.tecnologias === 'string' ? proyecto.tecnologias.split(',').map((t: string) => t.trim()) : []),
              }} />
              <button type="button" className="btn-email" onClick={() => setModalEmailOpen(true)}>
                📧 Enviar por Email
              </button>
            </div>
          </div>
        </div>
      </div>
      <ModalEnviarEmail
        open={modalEmailOpen}
        onClose={() => setModalEmailOpen(false)}
        onSend={handleSendEmail}
        loading={loadingEmail}
      />
      {toast && (
        <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />
      )}
    </>
  );
};

export default ModalResultadoRiesgo;
