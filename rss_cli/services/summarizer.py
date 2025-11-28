import logging
from typing import Optional

from groq import Groq
from rss_cli.config import API_GROQ_KEY

logger = logging.getLogger(__name__)

_client: Optional[Groq] = None

def get_client() -> Optional[Groq]:
    global _client
    if _client is not None:
        return _client

    if not API_GROQ_KEY:
        logger.warning(
            "API_GROQ_KEY missing – summarizer will use RSS fallback instead of Groq."
        )
        return None

    _client = Groq(api_key=API_GROQ_KEY)
    return _client


def fallback_from_rss(entry: dict) -> str:
    summary = entry.get("summary") or ""
    if not summary:
        return "Missing article description – take a look full article in link."

    if len(summary) > 500:
        return summary[:500].rstrip() + "..."
    return summary


def build_prompt(entry: dict, language: str = "pl") -> str:
    title = entry.get("title") or ""
    summary = entry.get("summary") or ""
    link = entry.get("link") or ""

    if language == "pl":
        return (
            "Streść poniższy artykuł w 3–5 zdaniach po polsku, używając poprawnej polszczyzny. "
            "Nie dodawaj wstępów typu 'Poniżej przedstawiam streszczenie artykułu' "
            "ani 'Oto streszczenie artykułu'. Zacznij od konkretów.\n\n"
            f"Tytuł: {title}\n"
            f"Treść artykułu z RSS:\n{summary}"
        )
    else:
        return (
            "Summarize this article in 3–5 short sentences in English. "
            "Do NOT write any introductions like 'Here is the summary' or 'This article discusses'. "
            "Start immediately with the key facts.\n\n"
            f"Title: {title}\n"
            f"RSS content:\n{summary}"
        )

def summarize_entry(entry: dict, language: str = "pl") -> str:
    client = get_client()
    if client is None:
        return fallback_from_rss(entry)

    prompt = build_prompt(entry, language=language)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Jesteś asystentem, który tworzy krótkie i rzeczowe streszczenia artykułów."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=220,
        )

        content = response.choices[0].message.content
        if not content:
            logger.warning("Groq returned empty content – using RSS fallback.")
            return fallback_from_rss(entry)

        text = content.strip()

        intro_trash = [
            "Poniżej przedstawiam",
            "Oto streszczenie artykułu",
            "Poniżej znajduje się",
            "W artykule opisano",
            "Ten artykuł omawia",
            "W tym artykule",
        ]
        for phrase in intro_trash:
            if text.lower().startswith(phrase.lower()):
                text = text[len(phrase):].lstrip(" :,-.\n")
                break

        return text

    except Exception as e:
        logger.exception("[summarizer][GROQ ERROR] %s", e)
        return fallback_from_rss(entry)
