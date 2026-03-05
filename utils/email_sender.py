import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def enviar_reporte_email(destinatario: str, asunto: str, cuerpo: str, ruta_pdf: str):
    """
    Envía un reporte por email usando Gmail SMTP.
    Requiere las variables de entorno:
      - SMTP_EMAIL: tu dirección de Gmail
      - SMTP_PASSWORD: contraseña de aplicación de Google (NO tu contraseña normal)
    
    Para obtener la contraseña de aplicación:
      1. Ve a https://myaccount.google.com/apppasswords
      2. Crea una nueva contraseña de aplicación para "Correo"
      3. Copia la contraseña de 16 caracteres
    """
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not smtp_email or not smtp_password:
        raise Exception(
            "Las variables SMTP_EMAIL y SMTP_PASSWORD no están configuradas. "
            "Configúralas en el panel de Render con tu Gmail y contraseña de aplicación."
        )
    
    msg = MIMEMultipart()
    msg['From'] = f"RiskPredictor RPA <{smtp_email}>"
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Cuerpo HTML profesional
    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); padding: 20px; border-radius: 12px 12px 0 0;">
            <h2 style="color: white; margin: 0; font-size: 20px;">🛡️ RiskPredictor RPA</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0; font-size: 14px;">Reporte de Evaluación de Riesgos</p>
        </div>
        <div style="background: #f8fafc; padding: 20px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px;">
            <p style="color: #334155; line-height: 1.6;">{cuerpo}</p>
            <p style="color: #64748b; font-size: 13px; margin-top: 20px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
                📎 Se ha adjuntado el reporte completo en formato PDF.
            </p>
        </div>
        <p style="color: #94a3b8; font-size: 11px; text-align: center; margin-top: 15px;">
            Este correo fue enviado automáticamente por RiskPredictor RPA. No responda a este mensaje.
        </p>
    </div>
    """
    
    msg.attach(MIMEText(html_body, 'html'))

    # Adjuntar PDF
    with open(ruta_pdf, "rb") as f:
        part = MIMEApplication(f.read(), Name="reporte_riesgo.pdf")
        part['Content-Disposition'] = 'attachment; filename="reporte_riesgo.pdf"'
        msg.attach(part)

    # Enviar vía Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
