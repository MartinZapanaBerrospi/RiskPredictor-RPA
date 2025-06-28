import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def enviar_reporte_mailhog(destinatario, asunto, cuerpo, ruta_pdf):
    remitente = "noreply@localhost"
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    msg.attach(MIMEText(cuerpo, 'plain'))

    with open(ruta_pdf, "rb") as f:
        part = MIMEApplication(f.read(), Name="reporte.pdf")
        part['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        msg.attach(part)

    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)
