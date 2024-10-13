from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
import os

# Load environment variables from .env
load_dotenv()

class Envs:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_STARTTLS = os.getenv("MAIL_STARTTLS").lower() == 'false'  
    MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS").lower() == 'true'  

# Configure the SMTP connection
config = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_PORT=int(Envs.MAIL_PORT),
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_STARTTLS=Envs.MAIL_STARTTLS,
    MAIL_SSL_TLS=Envs.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="api/templates"
)

# Email sending function
async def send_register_email(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype="html"
    )

    fm = FastMail(config)
    await fm.send_message(message=message, template_name="email.html")

async def password_reset(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html',
    )
    
    fm = FastMail(config)
    await fm.send_message(message, template_name='password_reset.html')