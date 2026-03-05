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
  if (l === 'alto') return '#f43f5e';
  if (l === 'medio') return '#f59e0b';
  return '#10b981';
}

function getRiskBg(level: string): string {
  const l = level.toLowerCase();
  if (l === 'alto') return 'rgba(244, 63, 94, 0.12)';
  if (l === 'medio') return 'rgba(245, 158, 11, 0.12)';
  return 'rgba(16, 185, 129, 0.12)';
}

function getBarColor(value: number): string {
  if (value > 0.6) return '#f43f5e';
  if (value > 0.3) return '#f59e0b';
  return '#10b981';
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
        throw new Error(data.detail || 'No se pudo enviar el email');
      }
      setToast({ message: 'Reporte enviado exitosamente', type: 'success' });
      setModalEmailOpen(false);
    } catch (e: any) {
      setToast({ message: e.message || 'Error al enviar email', type: 'error' });
    } finally {
      setLoadingEmail(false);
    }
  };

  if (!open || !resultado) return null;

  const riskColor = getRiskColor(resultado.riesgo_general);
  const riskBg = getRiskBg(resultado.riesgo_general);

  return (
    <>
      <div className="modal-editar-proyecto-overlay">
        <div className="modal-editar-proyecto" style={{ maxWidth: 520, padding: 0 }}>
          
          {/* Header con gradiente */}
          <div style={{
            background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
            padding: '1.5rem 2rem',
            borderRadius: '16px 16px 0 0',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}>
            <div>
              <h3 style={{ color: 'white', margin: 0, fontSize: '1.2rem', fontWeight: 700 }}>
                Resultado de Predicción
              </h3>
              <p style={{ color: 'rgba(255,255,255,0.7)', margin: '4px 0 0', fontSize: '0.85rem' }}>
                Motor Analítico de Riesgos — XGBoost
              </p>
            </div>
            <button onClick={onClose} style={{
              background: 'rgba(255,255,255,0.15)',
              border: 'none',
              color: 'white',
              width: 32,
              height: 32,
              borderRadius: '50%',
              cursor: 'pointer',
              fontSize: '1.1rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: 0,
              minWidth: 'unset',
            }}>✕</button>
          </div>

          {/* Body */}
          <div style={{ padding: '1.5rem 2rem' }}>
            
            {/* Risk Badge */}
            <div style={{
              background: riskBg,
              color: riskColor,
              border: `1px solid ${riskColor}30`,
              borderRadius: '100px',
              padding: '0.6rem 1.5rem',
              fontWeight: 800,
              fontSize: '1.3rem',
              textAlign: 'center',
              marginBottom: '1.5rem',
              textTransform: 'uppercase' as const,
              letterSpacing: '0.05em',
            }}>
              Riesgo {resultado.riesgo_general}
            </div>

            {/* Probabilidades de Riesgo */}
            <div style={{ marginBottom: '1.5rem' }}>
              <p style={{
                fontSize: '0.8rem',
                fontWeight: 600,
                color: '#94a3b8',
                textTransform: 'uppercase' as const,
                letterSpacing: '0.5px',
                marginBottom: '0.8rem',
              }}>Distribución de Probabilidades</p>
              
              {Object.entries(resultado.probabilidades_riesgo).map(([key, value]) => (
                <div key={key} style={{ marginBottom: '0.8rem' }}>
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    fontSize: '0.9rem',
                    marginBottom: '0.3rem',
                    fontFamily: '"Inter", monospace',
                  }}>
                    <span style={{ color: '#cbd5e1', textTransform: 'capitalize' as const }}>{key}</span>
                    <span style={{ color: getBarColor(value), fontWeight: 700 }}>{(value * 100).toFixed(1)}%</span>
                  </div>
                  <div style={{
                    background: 'rgba(255,255,255,0.05)',
                    height: 8,
                    borderRadius: 4,
                    overflow: 'hidden',
                  }}>
                    <div style={{
                      height: '100%',
                      borderRadius: 4,
                      background: getBarColor(value),
                      width: `${Math.max(value * 100, 2)}%`,
                      transition: 'width 1s ease-out',
                    }} />
                  </div>
                </div>
              ))}
            </div>

            {/* Sobrecosto y Retraso */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '1rem',
              marginBottom: '1.5rem',
            }}>
              <div style={{
                background: 'rgba(244, 63, 94, 0.08)',
                border: '1px solid rgba(244, 63, 94, 0.2)',
                borderRadius: 12,
                padding: '1rem',
                textAlign: 'center',
              }}>
                <p style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase' as const, margin: '0 0 4px' }}>Sobrecosto</p>
                <p style={{ color: getBarColor(resultado.probabilidad_sobrecosto), fontSize: '1.5rem', fontWeight: 800, margin: 0 }}>
                  {(resultado.probabilidad_sobrecosto * 100).toFixed(1)}%
                </p>
              </div>
              <div style={{
                background: 'rgba(245, 158, 11, 0.08)',
                border: '1px solid rgba(245, 158, 11, 0.2)',
                borderRadius: 12,
                padding: '1rem',
                textAlign: 'center',
              }}>
                <p style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase' as const, margin: '0 0 4px' }}>Retraso</p>
                <p style={{ color: getBarColor(resultado.probabilidad_retraso), fontSize: '1.5rem', fontWeight: 800, margin: 0 }}>
                  {(resultado.probabilidad_retraso * 100).toFixed(1)}%
                </p>
              </div>
            </div>

            {/* Action Buttons */}
            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
              <ReportePDFButton formData={{
                ...proyecto,
                tecnologias: Array.isArray(proyecto.tecnologias)
                  ? proyecto.tecnologias
                  : (typeof proyecto.tecnologias === 'string' ? proyecto.tecnologias.split(',').map((t: string) => t.trim()) : []),
              }} />
              <button
                type="button"
                onClick={() => setModalEmailOpen(true)}
                style={{
                  flex: 1,
                  background: 'transparent',
                  border: '1px solid rgba(148, 163, 184, 0.2)',
                  color: '#cbd5e1',
                  padding: '0.7rem 1rem',
                  borderRadius: 8,
                  cursor: 'pointer',
                  fontWeight: 600,
                  fontSize: '0.9rem',
                }}
              >
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
