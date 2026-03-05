"""
Envío de emails usando Brevo (ex-Sendinblue) HTTP API.
No requiere SMTP — funciona en cualquier servidor incluido Render.

Pasos para configurar:
  1. Crear cuenta gratuita en https://www.brevo.com/
  2. Ir a Settings → SMTP & API → API Keys → Generate a new API key
  3. Agregar la variable BREVO_API_KEY en Render
  4. (La primera vez) Verificar el email remitente en Brevo → Settings → Senders → Add a sender
"""

import os
import json
import base64
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

def enviar_reporte_email(destinatario: str, asunto: str, cuerpo: str, ruta_pdf: str):
    """Envía un reporte con PDF adjunto usando Brevo HTTP API."""
    
    api_key = os.getenv("BREVO_API_KEY", "").strip()
    sender_email = os.getenv("SMTP_EMAIL", "").strip()
    
    if not api_key:
        raise Exception(
            "La variable BREVO_API_KEY no está configurada. "
            "Crea una cuenta gratuita en brevo.com y agrega tu API key en Render."
        )
    if not sender_email:
        raise Exception(
            "La variable SMTP_EMAIL no está configurada. "
            "Agrega tu email remitente (el mismo verificado en Brevo) en Render."
        )
    
    # Leer PDF y convertir a base64
    with open(ruta_pdf, "rb") as f:
        pdf_content = base64.b64encode(f.read()).decode("utf-8")
    
    # Cuerpo HTML profesional
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
    
    payload = {
        "sender": {
            "name": "RiskPredictor RPA",
            "email": sender_email
        },
        "to": [
            {"email": destinatario}
        ],
        "subject": asunto,
        "htmlContent": html_body,
        "attachment": [
            {
                "content": pdf_content,
                "name": "reporte_riesgo.pdf"
            }
        ]
    }
    
    data = json.dumps(payload).encode("utf-8")
    
    req = Request(BREVO_API_URL, data=data, method="POST")
    req.add_header("accept", "application/json")
    req.add_header("content-type", "application/json")
    req.add_header("api-key", api_key)
    
    try:
        print(f"[EMAIL] Enviando a {destinatario} via Brevo API...")
        response = urlopen(req, timeout=15)
        result = json.loads(response.read().decode("utf-8"))
        print(f"[EMAIL] Enviado exitosamente. MessageId: {result.get('messageId', 'N/A')}")
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"[EMAIL] Error Brevo: {e.code} - {error_body}")
        raise Exception(
            f"Error enviando email via Brevo (HTTP {e.code}): {error_body}"
        )
    except Exception as e:
        print(f"[EMAIL] Error inesperado: {e}")
        raise Exception(f"Error enviando email: {e}")
