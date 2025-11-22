from groq import Groq
from config import API_GROQ_KEY

_client = None
if API_GROQ_KEY:
    _client = Groq(api_key=API_GROQ_KEY)
else:
    raise RuntimeError("Brak API_GROQ_KEY w .env – wymagany dla AI summarizer.")

def fallback_from_rss(entry: dict) -> str:
    summary = entry.get("summary") or ""
    if not summary:
        return "Brak opisu artykułu w RSS – przeczytaj pełny tekst pod linkiem."

    if len(summary) > 500:
        return summary[:500].rstrip() + "..."
    return summary


def build_prompt(entry: dict) -> str:
    return (
        "Streść poniższy artykuł w kilku krótkich zdaniach po polsku żywając przy tym poprawnej gramatyk. "
        "Podaj najważniejsze informacje, bez lania wody.\n\n"
        f"Tytuł: {entry.get('title')}\n"
        f"Link: {entry.get('link')}\n\n"
        f"Treść:\n{entry.get('summary')}"
    )


def summarize_entry(entry: dict, language: str = "pl") -> str:
    prompt = build_prompt(entry)

    try:
        response = _client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Jesteś asystentem, który tworzy krótkie i rzeczowe streszczenia artykułów."
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=220,
        )

        content = response.choices[0].message.content
        if not content:
            return fallback_from_rss(entry)

        return content.strip()

    except Exception as e:
        print(f"[summarizer][GROQ ERROR] {e}")
        return fallback_from_rss(entry)