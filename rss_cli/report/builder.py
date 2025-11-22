from rss_cli.summarizer import summarize_entry

class ReportBuilder:
    def __init__(self, language: str = "pl"):
        self.language = language

    def build(self, entries: list[dict]) -> str:
        if not entries:
            return "Brak wpisów po filtracji lub nieprawidłowy kanał RSS."

        lines: list[str] = []
        for index, entry in enumerate(entries, start=1):
            summary = summarize_entry(entry, language=self.language)

            lines.append(f"{index})")
            lines.append(f"Tytuł: {entry['title']}")
            lines.append(f"Link: {entry['link']}")
            lines.append("Streszczenie:")
            lines.append(summary)
            lines.append("")

        return "\n".join(lines)
