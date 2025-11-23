from dataclasses import dataclass
from rss_cli.config import config_message
from rss_cli.mailer import send_email

@dataclass
class EmailReportNotifier:
    subject_template: str | None = config_message[0]
    to_address: str | None = config_message[1]

    def __post_init__(self):
        if not self.to_address:
            raise RuntimeError("MSG_ADDRESS nie jest ustawione w .env – nie można wysłać raportu mailem.")

    def send_report(self, report_body: str, feed_url: str) -> None:
        subject = self.subject_template or f"RSS report for {feed_url}"
        send_email(subject=subject,body=report_body,to_address=self.to_address,)
