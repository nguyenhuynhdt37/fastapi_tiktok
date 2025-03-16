import aiosmtplib
from email.message import EmailMessage
from app.libs import renderTemplete
from app.libs.renderTemplete import render_template
from dotenv import load_dotenv
import os
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


print(EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT)


async def send_email(to_email: str, subject: str, template_name: str, **context):
    # Render template
    body = render_template(template_name, **context)

    # Tạo email message
    message = EmailMessage()
    # người gửi, người nhận, tiêu đề, nội dung
    message["From"] = EMAIL_ADDRESS
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body, subtype="html")  # Sử dụng HTML content

    # Gửi email
    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=EMAIL_ADDRESS,
            password=EMAIL_PASSWORD,
            start_tls=True,
        )
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
