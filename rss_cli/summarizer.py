from groq import Groq
from config import API_GROQ_KEY

_client = None
if API_GROQ_KEY:
    _client = Groq(api_key=API_GROQ_KEY)
else:
    raise RuntimeError("Missing API_GROQ_KEY in .env - It's AI summarizer requirments.")

def fallback_from_rss(entry: dict) -> str:
    summary = entry.get("summary") or ""
    if not summary:
        return "Missing article description – take a look on full article beside the link."

    if len(summary) > 500:
        return summary[:500].rstrip() + "..."
    return summary


def build_prompt(entry: dict, language: str = "pl") -> str:

    title = entry.get("title") or ""
    summary = entry.get("summary") or ""
    link = entry.get("link") or ""

    if language == "pl":
        return (
            "Streść poniższy artykuł w 3–5 zdaniach po polsku uzywając poprawnej polszczyzny."
            "Czyli np. nie powtarzaj wyrazów/nazw/imion/itp. bez potrzeby. "
            "Podaj wyłącznie treść streszczenia - bez żadnych wstępów, "
            "bez formułek typu 'Poniżej przedstawiam streszczenie', "
            "'Oto streszczenie artykułu', 'W tym artykule' lub podobnych. "
            "Zacznij natychmiast od konkretów.\n\n"
            f"Tytuł: {title}\n"
            f"Treść artykułu z RSS:\n{summary}"
        )

    else:
        return (
            "Summarize this article in 3–5 short sentences in English. "
            "Do NOT write any introductions like 'Here is the summary', "
            "'Below is the summary', or 'This article discusses'. "
            "Start immediately with the key facts.\n\n"
            f"Title: {title}\n"
            f"RSS content:\n{summary}"
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