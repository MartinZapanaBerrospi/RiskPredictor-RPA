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
        top: 24,
        right: 24,
        zIndex: 99999,
        minWidth: 300,
        maxWidth: 420,
        background: isSuccess
          ? "linear-gradient(135deg, rgba(16,185,129,0.95), rgba(5,150,105,0.95))"
          : "linear-gradient(135deg, rgba(239,68,68,0.95), rgba(220,38,38,0.95))",
        backdropFilter: "blur(12px)",
        color: "white",
        padding: "16px 20px",
        borderRadius: 12,
        boxShadow: isSuccess
          ? "0 8px 32px rgba(16,185,129,0.3), 0 2px 8px rgba(0,0,0,0.1)"
          : "0 8px 32px rgba(239,68,68,0.3), 0 2px 8px rgba(0,0,0,0.1)",
        cursor: "pointer",
        animation: "toastSlideIn 0.35s cubic-bezier(0.16,1,0.3,1)",
        display: "flex",
        alignItems: "flex-start",
        gap: 12,
        fontFamily: "'Inter', sans-serif",
      }}
      onClick={onClose}
      role="alert"
      aria-live="assertive"
    >
      {/* Icon */}
      <div style={{
        width: 28, height: 28, borderRadius: 8,
        background: "rgba(255,255,255,0.2)",
        display: "flex", alignItems: "center", justifyContent: "center",
        flexShrink: 0, marginTop: 1,
        fontSize: 14, fontWeight: 700,
      }}>
        {isSuccess ? "✓" : "✕"}
      </div>

      {/* Content */}
      <div style={{ flex: 1 }}>
        <div style={{ fontWeight: 600, fontSize: 14, lineHeight: 1.4 }}>
          {message}
        </div>
        {details && (
          <div style={{ fontSize: 13, opacity: 0.85, marginTop: 4, lineHeight: 1.3 }}>
            {details}
          </div>
        )}
      </div>

      {/* Close */}
      <div style={{
        opacity: 0.6, fontSize: 16, marginTop: -2,
        flexShrink: 0, fontWeight: 300,
      }}>
        ✕
      </div>

      <style>{`
        @keyframes toastSlideIn {
          from { opacity: 0; transform: translateX(40px) scale(0.96); }
          to { opacity: 1; transform: translateX(0) scale(1); }
        }
      `}</style>
    </div>
  );
};

export default Toast;
