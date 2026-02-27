from pathlib import Path

from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail

from app.core.config import app_settings
from app.models.users import User



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
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates_html/mails"
)


# send function async mandatory


# Welcome new user ===============================================================
async def send_welcome_email(user: User):
    message = MessageSchema(
        subject="Welcome !",
        recipients=[user.email],
        # body=f"<p>Welcome <strong>{username}</strong> !</p>",
        template_body={"user": user},
        subtype=MessageType.html,
    )

    fm = FastMail(mail_conf)
    await fm.send_message(message, template_name="welcome.html")


# Say to user he is reported =====================================================
async def send_report_user_email_details(user: User):
    message = MessageSchema(
        subject="You have been reported.",
        recipients=[user.email],
        #body=f"Hello {username} your account is reported.",
        subtype=MessageType.html,
        template_body={"user":user}
    )
    fm = FastMail(mail_conf)
    await fm.send_message(message, template_name="user_reported.html")
