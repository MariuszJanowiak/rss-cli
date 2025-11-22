import smtplib
from decorators import send_mail_validator
from email.message import EmailMessage
from config import SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

@send_mail_validator("SMTP_HOST", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD")
def send_email(subject: str, body: str, to_address: str, from_address: str | None = None):

    """
    subject - title of the message
    body - actual email message
    to_address - target email address where message have to go
    from_address - our SMTP address :)
    """

    ### Edges
    if not from_address: from_address = SMTP_USERNAME

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["To"] = to_address
    msg["From"] = from_address
    msg.set_content(body)

    ### Connect with SMTP server
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls() # Start encoding message
        server.login(SMTP_USERNAME, SMTP_PASSWORD) # log to sender email account
        server.send_message(msg) # Sending message