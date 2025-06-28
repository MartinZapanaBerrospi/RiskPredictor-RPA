import React, { useState } from "react";

interface ModalEnviarEmailProps {
  open: boolean;
  onClose: () => void;
  onSend: (email: string) => Promise<void>;
  loading: boolean;
}

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const ModalEnviarEmail: React.FC<ModalEnviarEmailProps> = ({ open, onClose, onSend, loading }) => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  const handleSend = async () => {
    if (!emailRegex.test(email)) {
      setError("Ingrese un email válido");
      return;
    }
    setError("");
    await onSend(email);
  };

  if (!open) return null;
  return (
    <div className="modal-editar-proyecto-overlay">
      <div className="modal-editar-proyecto" style={{ maxWidth: 400, padding: 32, borderRadius: 16, boxShadow: "0 8px 32px rgba(0,0,0,0.18)" }}>
        <h3 style={{ marginBottom: 16 }}>Enviar reporte por email</h3>
        <input
          type="email"
          placeholder="Correo electrónico"
          value={email}
          onChange={e => setEmail(e.target.value)}
          style={{
            width: "100%",
            padding: "12px 16px",
            borderRadius: 8,
            border: error ? "1.5px solid #e74c3c" : "1.5px solid #ccc",
            marginBottom: 8,
            fontSize: 16,
            outline: "none",
            boxSizing: "border-box"
          }}
          disabled={loading}
        />
        {error && <div style={{ color: "#e74c3c", fontSize: 14, marginBottom: 8 }}>{error}</div>}
        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 8 }}>
          <button
            type="button"
            className="cancel"
            onClick={onClose}
            disabled={loading}
            style={{ borderRadius: 8, padding: "8px 18px" }}
          >
            Cancelar
          </button>
          <button
            type="button"
            className="primary"
            onClick={handleSend}
            disabled={loading}
            style={{ borderRadius: 8, padding: "8px 18px", background: "#2d7be5", color: "white", fontWeight: 600, boxShadow: loading ? "none" : "0 2px 8px rgba(45,123,229,0.08)" }}
          >
            {loading ? "Enviando..." : "Enviar"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ModalEnviarEmail;
