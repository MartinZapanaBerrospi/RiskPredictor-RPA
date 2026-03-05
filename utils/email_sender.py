import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def enviar_reporte_email(destinatario: str, asunto: str, cuerpo: str, ruta_pdf: str):
    """
    Envía un reporte por email usando Gmail/Google Workspace SMTP.
    
    Variables de entorno requeridas:
      - SMTP_EMAIL: tu dirección (Gmail o Google Workspace, ej: user@uni.pe)
      - SMTP_PASSWORD: contraseña de aplicación de 16 caracteres
    """
    smtp_email = os.getenv("SMTP_EMAIL", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip()
    
    if not smtp_email or not smtp_password:
        raise Exception(
            "Las variables SMTP_EMAIL y SMTP_PASSWORD no están configuradas en Render."
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
            Este correo fue enviado automáticamente por RiskPredictor RPA.
        </p>
    </div>
    """
    
    msg.attach(MIMEText(html_body, 'html'))

    # Adjuntar PDF
    with open(ruta_pdf, "rb") as f:
        part = MIMEApplication(f.read(), Name="reporte_riesgo.pdf")
        part['Content-Disposition'] = 'attachment; filename="reporte_riesgo.pdf"'
        msg.attach(part)

    # Intentar con STARTTLS en puerto 587 (más compatible con Google Workspace)
    # Si falla, intentar SSL directo en puerto 465
    last_error = None
    
    for method in ["starttls", "ssl"]:
        try:
            if method == "starttls":
                server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
                server.ehlo()
                server.starttls()
                server.ehlo()
            else:
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15)
            
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
            server.quit()
            return  # Éxito
        except Exception as e:
            last_error = e
            try:
                server.quit()
            except Exception:
                pass
            continue

    raise Exception(
        f"No se pudo enviar el email. "
        f"Verifica que SMTP_EMAIL y SMTP_PASSWORD sean correctos. "
        f"Si usas un correo universitario (@uni.pe), asegúrate de que sea Google Workspace "
        f"y de haber generado la contraseña de aplicación desde tu cuenta. "
        f"Error: {last_error}"
    )
