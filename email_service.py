import os
import aiosmtplib
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP")

async def enviar_email_redefinicao(destinatario: str, token: str):
    link = f"http://localhost:8000/redefinir-senha?token={token}"

    mensagem = EmailMessage()
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = destinatario
    mensagem["Subject"] = "Redefinição de senha"

    mensagem.set_content(f"""
Olá!

Você solicitou a redefinição de senha.

Clique no link abaixo para redefinir sua senha:

{link}

Esse link expira em 30 minutos.

Caso você não tenha solicitado, ignore este e-mail.
""")

    await aiosmtplib.send(
        mensagem,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=EMAIL_REMETENTE,
        password=EMAIL_SENHA_APP
    )