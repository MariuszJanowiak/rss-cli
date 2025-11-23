from rss_cli.summarizer import summarize_entry
from datetime import datetime

class ReportBuilder:

    def __init__(self, language: str = "pl"):
        self.language = language

    def build_text(self, entries: list[dict]) -> str:
        if not entries:
            return "Couldn't found any posts related to inputs or RSS Channel is wrong."

        lines: list[str] = []
        for idx, entry in enumerate(entries, start=1):
            ai_summary = summarize_entry(entry, language=self.language)
            date_label = self.format_date(entry)

            title_line = f"{idx}) [{date_label}] {entry['title']}"
            link_line = f"Link: {entry['link']}"

            lines.append(title_line)
            lines.append(link_line)
            lines.append("Streszczenie:")
            lines.append(ai_summary)
            lines.append("")

        return "\n".join(lines)

    def build_html(self, entries: list[dict], feed_url: str | None = None) -> str:
        if not entries:
            return "<p>Couldn't found any posts related to inputs or RSS Channel is wrong.</p>"

        items_html: list[str] = []

        for idx, entry in enumerate(entries, start=1):
            ai_summary = summarize_entry(entry, language=self.language)
            date_label = self.format_date(entry)

            item = f"""
            <div style="margin-bottom: 24px;">
              <div style="font-size: 14px; color: #999;">#{idx}</div>
              <h3 style="margin: 4px 0 6px 0; font-size: 18px;">
                <span style="color:#666; font-weight: normal;">[{date_label}]</span>
                {entry['title']}
              </h3>
              <div style="margin-bottom: 6px;">
                <a href="{entry['link']}" style="color:#1a73e8; text-decoration:none;">
                  Otwórz artykuł
                </a>
              </div>
              <div style="font-size: 14px; line-height: 1.5; color:#333;">
                {ai_summary}
              </div>
            </div>
            """
            items_html.append(item)

        feed_info = f'<p style="font-size:12px; color:#777;">Źródło RSS: {feed_url}</p>' if feed_url else ""

        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background:#f5f5f5; padding:16px;">
            <div style="max-width: 800px; margin:0 auto; background:#ffffff; padding:20px; border-radius:8px;">
              <h2 style="margin-top:0; margin-bottom:8px;">Twój raport RSS</h2>
              {feed_info}
              <hr style="border:none; border-top:1px solid #ddd; margin:16px 0;" />
              {''.join(items_html)}
            </div>
          </body>
        </html>
        """
        return html.strip()

    @staticmethod
    def format_date(entry: dict) -> str:
        dt = entry.get("published_dt")
        if isinstance(dt, datetime):
            return dt.strftime("%Y-%m-%d")
        text = (entry.get("published") or "").strip()
        if not text:
            return "brak daty"
        return text[:16]
