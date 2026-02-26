from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail

from app.core.config import app_settings



mail_conf = ConnectionConfig(
    MAIL_USERNAME=app_settings.mail_username,
    MAIL_PASSWORD=app_settings.mail_password,
    MAIL_PORT=app_settings.mail_port,
    MAIL_FROM=app_settings.mail_from,
    MAIL_SERVER=app_settings.mail_host,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    # VALIDATE_CERTS=True,
)


# send function async mandatory

async def send_welcome_email(email: str, username: str):
    message = MessageSchema(
        subject="Welcome !",
        recipients=[email],
        body=f"<p>Welcome <strong>{username}</strong> !</p>",
        subtype=MessageType.html,
    )

    fm = FastMail(mail_conf)
    await fm.send_message(message)