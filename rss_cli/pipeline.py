from itertools import islice
from typing import Iterable, Iterator
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta

def lazy_iter_entries(parsed: dict) -> Iterator[dict]:
    for entry in parsed.get("entries", []):
        yield entry

def normalize_entry(entry: dict) -> dict:
    published_text = entry.get("published") or entry.get("updated") or "Brak daty"
    published_datetime = parse_published_datetime(entry)

    return {
        "id": entry.get("id") or entry.get("link") or entry.get("title", ""),
        "title": (entry.get("title") or "").strip(),
        "link": (entry.get("link") or "").strip(),
        "summary": (entry.get("summary") or entry.get("description") or "").strip(),
        "published": published_text,
        "published_datetime": published_datetime,
    }

def normalize_entries(entries: Iterable[dict]) -> Iterator[dict]:
    for entry in entries:
        yield normalize_entry(entry)

def filter_entries(entries: Iterable[dict], include=None, exclude=None) -> Iterator[dict]:
    include = [inc.lower() for inc in (include or [])]
    exclude = [exc.lower() for exc in (exclude or [])]

    for entry in entries:
        text = f"{entry['title']} {entry['summary']}".lower()
        if include and not any(word in text for word in include):
            continue
        if exclude and any(word in text for word in exclude):
            continue
        yield entry


# noinspection PyBroadException
def parse_published_datetime(entry: dict):
    structure = entry.get("published_parsed") or entry.get("updated_parsed")
    if structure:
        try:
            return datetime(*structure[:6], tzinfo=timezone.utc)
        except Exception:
            pass

    text = entry.get("published") or entry.get("updated")
    if not text:
        return None

    try:
        date = parsedate_to_datetime(text)

        if date is None:
            return None

        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        else:
            date = date.astimezone(timezone.utc)

        return date
    except Exception:
        return None


def filter_by_age(entries: Iterable[dict], old: int | None) -> Iterator[dict]:
    now = datetime.now(timezone.utc)
    max_delta = timedelta(days=old)

    for entry in entries:
        date = entry.get("published_datetime")
        if date is None:
            return None

        if now - date <= max_delta:
            yield entry
    return None


def build_pipeline( parsed: dict, old: int | None, include=None, exclude=None, limit: int | None = None) -> list[dict]:
    if old is not None:
        if old < 1: old = 1
        if old > 31: old = 31

    entries = lazy_iter_entries(parsed)
    entries = normalize_entries(entries)
    entries = filter_entries(entries, include, exclude)
    entries = filter_by_age(entries, old)

    if limit is not None and limit > 0:
        entries = islice(entries, limit)

    return list(entries)