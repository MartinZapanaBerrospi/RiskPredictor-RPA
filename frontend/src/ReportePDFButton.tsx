import React from "react";

type Props = {
  formData: any;
};

const ReportePDFButton: React.FC<Props> = ({ formData }) => {
  const handleGenerarReporte = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/generar-reporte", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...formData,
          tecnologias: formData.tecnologias.join(','),
          duracion_estimacion: Number(formData.duracion_estimacion),
          presupuesto_estimado: Number(formData.presupuesto_estimado),
          numero_recursos: Number(formData.numero_recursos),
          experiencia_equipo: Number(formData.experiencia_equipo),
          hitos_clave: Number(formData.hitos_clave),
        }),
      });
      if (!response.ok) throw new Error("Error al generar el reporte PDF");
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "reporte_riesgo.pdf");
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error: any) {
      alert(error.message);
    }
  };

  return (
    <button onClick={handleGenerarReporte} style={{marginTop: 16}}>
      Descargar reporte PDF
    </button>
  );
};

export default ReportePDFButton;
