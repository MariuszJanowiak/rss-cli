import argparse
import requests
import feedparser

def main():
    parser = (argparse.ArgumentParser(
        prog="rss_cli",
        description="MVP: pobierz kanał RSS i wypisz tytuły."
    ))

    parser.add_argument("--url", required=True, help="RSS channel URL")
    parser.add_argument("--limit", type=int, default=10, help="Posts limiter (default: 5")
    parser.add_argument("--include", help="Post Keywords require (separate by comma)")
    parser.add_argument("--exclude", help="Post Keywords unacceptable (separate by comma)")
    args = parser.parse_args()

    parsed = fetch_feed(args.url)
    pipeline(parsed, args)

def fetch_feed(url: str) -> dict:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return feedparser.parse(response.content)

def lazy_iter_entries(parsed: dict):
    for entry in parsed.get("entries", []):
        yield entry

def pipeline(parsed: dict, args=None):
    include = args.include.split(",") if args.include else []
    exclude = args.exclude.split(",") if args.exclude else []

    #pipeline
    entries = lazy_iter_entries(parsed)
    entries = normalize_entries(entries)
    entries = filter_entries(entries, include, exclude)

    counter = 0
    for entry in entries:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        print(f"- {title}\n  {link}\n")
        counter += 1
        if counter >= args.limit:
            break

    if counter == 0:
        print("Brak wpisów lub nieprawidłowy kanał RSS.")

def normalized_entry(entry: dict) -> dict:
    return {
        "id": entry.get("id") or entry.get("link") or entry.get("title", ""),
        "title": (entry.get("title") or "").strip(),
        "link": (entry.get("link") or "").strip(),
        "summary": (entry.get("summary") or entry.get("description") or "").strip(),
        "published": entry.get("published") or entry.get("updated") or "Brak daty",
    }

def normalize_entries(entries):
    for entry in entries:
        yield normalized_entry(entry)

def filter_entries(entries, include=None, exclude=None):
    include = [s.lower() for s in include or []]
    exclude = [s.lower() for s in exclude or []]

    for entry in entries:
        text = f"{entry['title']} {entry['summary']}".lower()

        if include and not any(word in text for word in include):
            continue
        if exclude and any(word in text for word in exclude):
            continue

        yield entry

if __name__ == "__main__":
    main()