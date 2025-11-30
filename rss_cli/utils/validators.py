import argparse
import logging
from dataclasses import dataclass
from rss_cli.config import SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, MSG_ADDRESS

logger = logging.getLogger(__name__)

class ValidationError(ValueError):
    """I/O Errors"""

class ConfigError(RuntimeError):
    """Configuration Errors"""

### CLI

def validate_cli_args(args: argparse.Namespace) -> None:
    errors: list[str] = []
    forbidden_substrings = ["feed", "atom", "rss"]

    # URL
    if not args.url:
        errors.append("--url is required.")
    elif args.url.startswith("http://"):
        errors.append("--url contain unsecure protocol http://")
    elif not (args.url.startswith("https://")):
        errors.append("--url must start with https://")
    elif not any(substring in args.url for substring in forbidden_substrings):
        errors.append("--url must be RSS or Atom Channel")

    # OLD
    if args.old is None:
        errors.append("--old is required.")
    elif not (1 <= args.old <= 31):
        errors.append("--old must be between 1 and 31 days.")

    # LIMIT
    if args.limit is not None and args.limit <= 0:
        errors.append("--limit must be a positive integer.")

    if errors:
        raise ValidationError("\n".join(errors))

### SMTP

@dataclass(frozen=True)
class SmtpConfig:
    host: str | None = SMTP_HOST
    port: int | None = SMTP_PORT
    username: str | None = SMTP_USERNAME
    password: str | None = SMTP_PASSWORD


def validate_smtp_config(config: SmtpConfig | None = None) -> None:
    cfg = config or SmtpConfig()
    missing: list[str] = []

    if not cfg.host:
        missing.append("SMTP_HOST")
    if not cfg.port:
        missing.append("SMTP_PORT")
    if not cfg.username:
        missing.append("SMTP_USERNAME")
    if not cfg.password:
        missing.append("SMTP_PASSWORD")

    if missing:
        raise ConfigError(
            f"Missing SMTP configuration values in .env: {', '.join(missing)}"
        )

def validate_recipient_address(address: str | None = None) -> None:
    addr = address or MSG_ADDRESS
    if not addr:
        raise ConfigError("MSG_ADDRESS is not set in .env – cannot send report.")
    if "@" not in addr:
        raise ValidationError(f"MSG_ADDRESS looks invalid: {addr!r}")