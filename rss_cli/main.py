import argparse

from fetch import fetch_feed
from report.builder import ReportBuilder
from report.notifier import EmailReportNotifier
from pipeline import build_pipeline

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="rss_cli",
        description="RSS news scrapper filtered by targeted keywords."
    )

    parser.add_argument("--url", required=True, help="RSS channel URL")
    parser.add_argument("--limit", type=int, default=10, help="Posts limiter (default: 10)")
    parser.add_argument("--include", help="Post required Keywords (separate by comma)")
    parser.add_argument("--exclude", help="Post unacceptable Keywords (separate by comma)")

    return parser.parse_args()

def main():
    # Input
    args = parse_args()

    # Feed
    parsed = fetch_feed(args.url)

    # Pipeline
    include = args.include.split(",") if args.include else []
    exclude = args.exclude.split(",") if args.exclude else []
    entries = build_pipeline(parsed, include=include, exclude=exclude, limit=args.limit)

    # Report
    builder = ReportBuilder(language="pl")
    report_body = builder.build(entries)

    # Mail sender
    notifier = EmailReportNotifier()
    notifier.send_report(report_body, feed_url=args.url)

    print("Report has been sent.")

if __name__ == "__main__":
    main()
