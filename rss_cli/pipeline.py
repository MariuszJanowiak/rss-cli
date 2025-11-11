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
    for e in entries:
        yield normalize_entry(e)

def filter_entries(entries: Iterable[dict], include=None, exclude=None) -> Iterator[dict]:
    include = [s.lower() for s in (include or [])]
    exclude = [s.lower() for s in (exclude or [])]

    for entry in entries:
        text = f"{entry['title']} {entry['summary']}".lower()
        if include and not any(word in text for word in include):
            continue
        if exclude and any(word in text for word in exclude):
            continue
        yield entry
