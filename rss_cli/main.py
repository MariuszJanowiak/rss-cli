import argparse
import logging
from logging_config import setup_logging

from rss_cli.core.fetch import fetch_feed
from rss_cli.core.pipeline import build_pipeline
from rss_cli.report.builder import ReportBuilder
from rss_cli.services.notifier import EmailReportNotifier
from rss_cli.utils.validators import validate_cli_args, ValidationError

logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="rss_cli",
        description="RSS news scrapper filtered by targeted keywords."
    )

    parser.add_argument("--url", required=True, help="RSS channel URL")
    parser.add_argument(
        "--old",
        type=int,
        required=True,
        help="How old News might be - limit equaled 31 DAYS",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Posts limiter (default: 10)",
    )
    parser.add_argument("--include", help="Post required Keywords (separate by comma)")
    parser.add_argument("--exclude", help="Post unacceptable Keywords (separate by comma)")

    return parser.parse_args()

def main():

    # Input
    args = parse_args()
    logger.info("Starting RSS CLI for url=%s, old=%s, limit=%s",
                args.url, args.old, args.limit)
    try:
        validate_cli_args(args)
    except ValidationError as e:
        print("Invalid arguments:\n")
        print(e)
        raise SystemExit(2)


    # Feed
    parsed = fetch_feed(args.url)

    # Pipeline
    include = args.include.split(",") if args.include else []
    exclude = args.exclude.split(",") if args.exclude else []
    entries = build_pipeline(
        parsed,
        old=args.old,
        include=include,
        exclude=exclude,
        limit=args.limit,
    )

    # Report
    builder = ReportBuilder(language="pl")
    text_body = builder.build_text(entries)
    html_body = builder.build_html(entries, feed_url=args.url)

    # Mail sender
    notifier = EmailReportNotifier()
    notifier.send_report(
        text_body=text_body,
        html_body=html_body,
        feed_url=args.url,
    )

    print("Email has been sent.")

if __name__ == "__main__":
    setup_logging()
    try:
        main()
    except Exception:
        logger.exception("Unhandled error in CLI:")
        raise SystemExit(1)
