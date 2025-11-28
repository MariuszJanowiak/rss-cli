# RSS News Email Reporter

`rss-cli` is a compact command-line utility that:

- Fetches articles from RSS feeds  
- Filters them by keywords and publication date  
- Generates short AI summaries (Groq), with RSS fallback  
- Builds a clean text and HTML report  
- Sends the report to a configured email address  

Perfect for daily monitoring of cybersecurity, finance, tech, business, or any domain with RSS sources.

## Installation

```bash
pip install -r requirements.txt
```

or inside a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Enviroment configuration
Create .env file in the project root:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

Notes:

* If `API_GROQ_KEY` is missing, summaries fall back to RSS `summary` content.
* Gmail users must use an **App Password** (not your real password).

---

## Usage

### Basic example

```bash
python -m rss_cli.main --url https://krebsonsecurity.com/feed/ --old 7
```

### Parameters

| Argument    | Required? | Description                                       |
| ----------- | --------- | ------------------------------------------------- |
| `--url`     | YES       | RSS feed URL                                      |
| `--old`     | YES       | Maximum article age in days (1–31)                |
| `--limit`   | No        | Max number of articles (default: 10)              |
| `--include` | No        | Comma-separated keywords that MUST appear         |
| `--exclude` | No        | Comma-separated keywords that disqualify the post |

---

## Examples

### Fetch articles from last 7 days

```bash
python -m rss_cli.main \
    --url https://krebsonsecurity.com/feed/ \
    --old 7
```

### Filter Windows-security content, limit to 5

```bash
python -m rss_cli.main \
    --url https://krebsonsecurity.com/feed/ \
    --old 7 \
    --limit 5 \
    --include "windows,security"
```

### Exclude sponsored content

```bash
python -m rss_cli.main \
    --url https://example.com/rss \
    --old 10 \
    --exclude "sponsored,advertisement"
```

### Cybersecurity-themed report

```bash
python -m rss_cli.main \
    --url https://example.com/cyber/rss \
    --old 3 \
    --include "cve,ransomware,zero-day"
```

## How It Works

1. **Fetch RSS feed** using `requests + feedparser`.
2. **Normalize entries** (title, link, summary, published date).
3. **Filter** using:

   * include keywords
   * exclude keywords
   * publication date ("old")
   * article limit
4. **Summarize articles**:

   * AI (Groq model)
   * or fallback to RSS summary
5. **Generate report**:

   * plain text (for email body text)
   * HTML (for rich formatting)
6. **Send email** via SMTP.

---

## Error Handling

* Incorrect CLI arguments → clear error message.
* Missing `.env` configuration → explicit configuration error.
* AI summarization failure → fallback to RSS summary.
* All errors logged in `logs/rss_cli.log`.

---

## Project Structure

```
rss-cli/
  rss_cli/
    core/
      __init__.py
      fetch.py
      pipeline.py
    report/
      builder.py
    services/
      __init__.py
      mailer.py
      notifier.py
      summarizer.py
    utils/
      __init__.py
      decorators.py
      validators.py
    __init__.py
    config.py
    logging_config.py
    main.py
  tests/
  .env
  .gitignore
  README.md
  requirments.txt

```
