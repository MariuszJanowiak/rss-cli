import smtplib
from rss_cli.utils.decorators import send_mail_validator
from email.message import EmailMessage
from rss_cli.config import SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD


@send_mail_validator("SMTP_HOST", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD")
def send_email(
    subject: str,
    body_text: str,
    to_address: str,
    from_address: str | None = None,
    body_html: str | None = None,
):

    ### Edge
    if not from_address: from_address = SMTP_USERNAME

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["To"] = to_address
    msg["From"] = from_address

    if body_html:
        msg.set_content(body_text or "Zobacz wersję HTML wiadomości.")
        msg.add_alternative(body_html, subtype="html")
    else:
        msg.set_content(body_text)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)