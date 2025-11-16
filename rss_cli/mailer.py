import smtplib
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
# Protocols:
# 587 - TLS
# 465 - SSL
SMTP_USERNAME = "Agent_mailer@gmail.com"
SMTP_PASSWORD = "Super_hidden_password123!"

def send_email(subject: str, body: str, to_address: str, from_address: str | None = None):
    """
    subject - title of the message
    body - actual email message
    to_address - target email address where message have to go
    from_address - our SMTP address :)
    """

    # Edges
    if not from_address:
        from_address = SMTP_USERNAME

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["To"] = to_address
    msg["From"] = from_address
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls() # Start encoding message
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD) # log to sender email account
        smtp.send_message(msg)