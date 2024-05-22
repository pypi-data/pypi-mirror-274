import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.configuration.configuration import TO_EMAIL


def alerts_smtp(subject, message, to_email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'geovanne.zanata@btime.com.br'
    smtp_password = 'geomhz97'

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print("Email enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar email:", e)


def send_email(message_error, status_error, start_time_error, end_time_error, description_error, rpa_id_error):
    subject = f"ERROR LOG - {status_error}"
    message = f"ERRO NO LOG:\n\n{message_error}\nSTATUS: {status_error}\nINICIO DA EXECUÇÃO: {start_time_error}\nHORÁRIO DO ERRO: {end_time_error}\nDESCRICAO: {description_error}\nRPA_ID: {rpa_id_error}"
    to_email = TO_EMAIL
    for email in to_email:
        alerts_smtp(subject, message, email)
