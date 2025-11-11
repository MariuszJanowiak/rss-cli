import argparse

from fetch import fetch_feed
from pipeline import lazy_iter_entries, normalize_entries, filter_entries

def main():
    parser = (argparse.ArgumentParser(
        prog="rss_cli",
        description="MVP: Download news from RSS channels filtering them by targeted keywords."
    ))

    parser.add_argument("--url", required=True, help="RSS channel URL")
    parser.add_argument("--limit", type=int, default=10, help="Posts limiter (default: 5")
    parser.add_argument("--include", help="Post required Keywords (separate by comma)")
    parser.add_argument("--exclude", help="Post unacceptable Keywords (separate by comma)")
    args = parser.parse_args()

    parsed = fetch_feed(args.url)
    entries = build_pipeline(parsed, args)

    counter = 0
    for entry in entries:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        print(f"- {title}\n  {link}\n")
        counter += 1
        if counter >= args.limit:
            break

    if counter == 0:
        print("Lack of articles or wrong channel RSS - Try again later.")

def build_pipeline(parsed: dict, args=None):
    include = args.include.split(",") if args.include else []
    exclude = args.exclude.split(",") if args.exclude else []

    # pipeline
    entries = lazy_iter_entries(parsed)
    entries = normalize_entries(entries)
    entries = filter_entries(entries, include, exclude)
    return entries

if __name__ == "__main__":
    main()