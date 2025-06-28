import React from "react";

interface ToastProps {
  message: string;
  type?: "success" | "error";
  onClose: () => void;
}

const Toast: React.FC<ToastProps> = ({ message, type = "success", onClose }) => {
  React.useEffect(() => {
    const timer = setTimeout(onClose, 3500);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div
      style={{
        position: "fixed",
        top: 32,
        right: 32,
        zIndex: 9999,
        background: type === "success" ? "#2ecc40" : "#e74c3c",
        color: "white",
        padding: "14px 28px",
        borderRadius: 12,
        fontWeight: 600,
        fontSize: 16,
        boxShadow: "0 4px 24px rgba(0,0,0,0.13)",
        minWidth: 220,
        display: "flex",
        alignItems: "center",
        gap: 12,
        cursor: "pointer"
      }}
      onClick={onClose}
    >
      {type === "success" ? (
        <span style={{ fontSize: 20, marginRight: 6 }}>✔️</span>
      ) : (
        <span style={{ fontSize: 20, marginRight: 6 }}>❌</span>
      )}
      {message}
    </div>
  );
};

export default Toast;
