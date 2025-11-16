from typing import Iterable, Iterator

def lazy_iter_entries(parsed: dict) -> Iterator[dict]:
    for entry in parsed.get("entries", []):
        yield entry

def normalize_entry(entry: dict) -> dict:
    return {
        "id": entry.get("id") or entry.get("link") or entry.get("title", ""),
        "title": (entry.get("title") or "").strip(),
        "link": (entry.get("link") or "").strip(),
        "summary": (entry.get("summary") or entry.get("description") or "").strip(),
        "published": entry.get("published") or entry.get("updated") or "Brak daty",
    }

def normalize_entries(entries: Iterable[dict]) -> Iterator[dict]:
    for entry in entries:
        yield normalize_entry(entry)

def filter_entries(entries: Iterable[dict], include=None, exclude=None) -> Iterator[dict]:
    include = [position_included.lower() for position_included in (include or [])]
    exclude = [position_excluded.lower() for position_excluded in (exclude or [])]

    for entry in entries:
        text = f"{entry['title']} {entry['summary']}".lower()
        if include and not any(word in text for word in include):
            continue
        if exclude and any(word in text for word in exclude):
            continue
        yield entry
