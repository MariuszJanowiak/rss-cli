import argparse
import logging
import textwrap

from rss_cli.logging_config import setup_logging
from rss_cli.core.fetch import fetch_feed
from rss_cli.core.pipeline import build_pipeline
from rss_cli.report.builder import ReportBuilder
from rss_cli.services.notifier import EmailReportNotifier
from rss_cli.utils.validators import validate_cli_args, ValidationError

logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="rss-cli",
        description=(
            "A command-line tool for fetching RSS feeds, filtering articles, "
            "summarizing content using AI, and sending a consolidated report via email."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:

              1) Fetch articles from the last 7 days:
                 python -m rss_cli.main \\
                     --url https://krebsonsecurity.com/feed/ \\
                     --old 7

              2) Filter only Windows-related security topics (max 5 articles):
                 python -m rss_cli.main \\
                     --url https://krebsonsecurity.com/feed/ \\
                     --old 7 \\
                     --limit 5 \\
                     --include "windows,security"

              3) Exclude sponsored posts:
                 python -m rss_cli.main \\
                     --url https://example.com/rss \\
                     --old 10 \\
                     --exclude "sponsored,advertisement"

              4) Cybersecurity-specific report:
                 python -m rss_cli.main \\
                     --url https://example.com/cyber/rss \\
                     --old 3 \\
                     --include "cve,ransomware,zero-day"
            """
        ),
    )

    parser.add_argument(
        "--url",
        required=True,
        metavar="RSS_URL",
        help="REQUIRED: URL of the RSS feed/atom",
    )

    parser.add_argument(
        "--old",
        type=int,
        required=True,
        metavar="DAYS",
        help="REQUIRED: Maximum article age in days (1–31). Example: 7 = last week only.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        metavar="N",
        help="OPTIONAL: Maximum number of articles included in the report (default: 5).",
    )

    parser.add_argument(
        "--include",
        metavar="KEYWORDS",
        help=(
            "OPTIONAL: Comma-separated list of keywords that MUST appear in the article title or summary.\n"
            'Example: "cve,ransomware,linux".'
        ),
    )

    parser.add_argument(
        "--exclude",
        metavar="KEYWORDS",
        help=(
            "OPTIONAL : Comma-separated list of keywords that automatically EXCLUDE an article.\n"
            'Example: "sponsored,advertisement".'
        ),
    )

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
        limit=args.limit
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