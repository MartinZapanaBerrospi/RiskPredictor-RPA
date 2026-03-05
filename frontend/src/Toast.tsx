import React from "react";

interface ToastProps {
  message: string;
  type?: "success" | "error";
  onClose: () => void;
  details?: string;
}

const Toast: React.FC<ToastProps> = ({ message, type = "success", onClose, details }) => {
  React.useEffect(() => {
    const timer = setTimeout(onClose, 5000);
    return () => clearTimeout(timer);
  }, [onClose]);

  const isSuccess = type === "success";

  return (
    <div
      style={{
        position: "fixed",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        zIndex: 99999,
        minWidth: 320,
        maxWidth: 440,
        background: isSuccess
          ? "linear-gradient(135deg, #059669, #10b981)"
          : "linear-gradient(135deg, #dc2626, #ef4444)",
        color: "white",
        padding: "20px 24px",
        borderRadius: 16,
        boxShadow: isSuccess
          ? "0 20px 60px rgba(16,185,129,0.4), 0 4px 16px rgba(0,0,0,0.15)"
          : "0 20px 60px rgba(239,68,68,0.4), 0 4px 16px rgba(0,0,0,0.15)",
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        gap: 14,
        fontFamily: "'Inter', sans-serif",
        animation: "toastPop 0.3s cubic-bezier(0.16,1,0.3,1)",
      }}
      onClick={onClose}
      role="alert"
      aria-live="assertive"
    >
      {/* Icon */}
      <div style={{
        width: 36, height: 36, borderRadius: 10,
        background: "rgba(255,255,255,0.2)",
        display: "flex", alignItems: "center", justifyContent: "center",
        flexShrink: 0, fontSize: 18, fontWeight: 700,
      }}>
        {isSuccess ? "✓" : "✕"}
      </div>

      {/* Content */}
      <div style={{ flex: 1 }}>
        <div style={{ fontWeight: 700, fontSize: 15, lineHeight: 1.4 }}>
          {message}
        </div>
        {details && (
          <div style={{ fontSize: 13, opacity: 0.85, marginTop: 4 }}>
            {details}
          </div>
        )}
        <div style={{ fontSize: 12, opacity: 0.6, marginTop: 6 }}>
          Clic para cerrar
        </div>
      </div>

      <style>{`
        @keyframes toastPop {
          from { opacity: 0; transform: translate(-50%, -50%) scale(0.9); }
          to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
        }
      `}</style>
    </div>
  );
};

export default Toast;
