import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def enviar_reporte_email(destinatario: str, asunto: str, cuerpo: str, ruta_pdf: str):
    """
    Envía un reporte por email usando Gmail SMTP.
    """
    smtp_email = os.getenv("SMTP_EMAIL", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip().replace(" ", "")
    
    print(f"[EMAIL] Intentando enviar a: {destinatario}")
    print(f"[EMAIL] Usando remitente: {smtp_email}")
    print(f"[EMAIL] Password length: {len(smtp_password)} chars")
    
    if not smtp_email or not smtp_password:
        raise Exception(
            "Las variables SMTP_EMAIL y SMTP_PASSWORD no están configuradas en Render."
        )
    
    msg = MIMEMultipart()
    msg['From'] = f"RiskPredictor RPA <{smtp_email}>"
    msg['To'] = destinatario
    msg['Subject'] = asunto

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); padding: 20px; border-radius: 12px 12px 0 0;">
            <h2 style="color: white; margin: 0; font-size: 20px;">RiskPredictor RPA</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0; font-size: 14px;">Reporte de Evaluacion de Riesgos</p>
        </div>
        <div style="background: #f8fafc; padding: 20px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px;">
            <p style="color: #334155; line-height: 1.6;">{cuerpo}</p>
            <p style="color: #64748b; font-size: 13px; margin-top: 20px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
                Se ha adjuntado el reporte completo en formato PDF.
            </p>
        </div>
    </div>
    """
    
    msg.attach(MIMEText(html_body, 'html'))

    with open(ruta_pdf, "rb") as f:
        part = MIMEApplication(f.read(), Name="reporte_riesgo.pdf")
        part['Content-Disposition'] = 'attachment; filename="reporte_riesgo.pdf"'
        msg.attach(part)

    errors = []
    
    # Intento 1: STARTTLS puerto 587
    server = None
    try:
        print("[EMAIL] Intentando STARTTLS puerto 587...")
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()
        print("[EMAIL] Enviado exitosamente via STARTTLS 587")
        return
    except Exception as e:
        errors.append(f"STARTTLS:587 -> {type(e).__name__}: {e}")
        print(f"[EMAIL] STARTTLS fallo: {e}")
        try:
            if server: server.quit()
        except Exception:
            pass

    # Intento 2: SSL directo puerto 465
    server = None
    try:
        print("[EMAIL] Intentando SSL puerto 465...")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15)
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()
        print("[EMAIL] Enviado exitosamente via SSL 465")
        return
    except Exception as e:
        errors.append(f"SSL:465 -> {type(e).__name__}: {e}")
        print(f"[EMAIL] SSL fallo: {e}")
        try:
            if server: server.quit()
        except Exception:
            pass

    error_detail = " | ".join(errors)
    raise Exception(
        f"No se pudo enviar el email. {error_detail}"
    )
