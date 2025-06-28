import React from "react";

interface ToastProps {
  message: string;
  type?: "success" | "error";
  onClose: () => void;
  details?: string;
}

const Toast: React.FC<ToastProps> = ({ message, type = "success", onClose, details }) => {
  React.useEffect(() => {
    const timer = setTimeout(onClose, 3500);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div
      style={{
        position: "fixed",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        zIndex: 9999,
        background: type === "success" ? "#005fa3" : "#e74c3c",
        color: "white",
        padding: details ? "22px 38px 18px 38px" : "18px 36px",
        borderRadius: 18,
        fontWeight: 700,
        fontSize: 18,
        boxShadow: "0 8px 40px #00336633, 0 2px 12px #005fa322",
        minWidth: 260,
        maxWidth: 420,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 10,
        cursor: "pointer",
        textAlign: "center",
        letterSpacing: 0.2,
        transition: "background 0.2s, box-shadow 0.2s"
      }}
      onClick={onClose}
      role="alert"
      aria-live="assertive"
    >
      <div style={{display: 'flex', alignItems: 'center', gap: 12, fontSize: 22, marginBottom: 2}}>
        {type === "success" ? (
          <span style={{ fontSize: 22 }}>✔️</span>
        ) : (
          <span style={{ fontSize: 22 }}>❌</span>
        )}
        <span style={{fontWeight: 700, fontSize: 18}}>{message}</span>
      </div>
      {details && (
        <div style={{fontWeight: 400, fontSize: 15, color: '#eaf3fb', marginTop: 4, opacity: 0.92}}>{details}</div>
      )}
      <span style={{fontSize: 13, marginTop: 8, opacity: 0.7}}>Clic para cerrar</span>
    </div>
  );
};

export default Toast;
