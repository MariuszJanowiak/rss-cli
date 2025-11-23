from dataclasses import dataclass
from rss_cli.config import config_message
from rss_cli.services.mailer import send_email
from rss_cli.utils.validators import validate_recipient_address

@dataclass
class EmailReportNotifier:
    subject_template: str | None = config_message[0]
    to_address: str | None = config_message[1]

    def __post_init__(self):
        validate_recipient_address(self.to_address)

    def send_report(self, text_body: str, html_body: str, feed_url: str,):
        subject = self.subject_template or f"RSS report for {feed_url}"

        send_email(
            subject=subject,
            body_text=text_body,
            body_html=html_body,
            to_address=self.to_address,
        )