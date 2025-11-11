import requests
import feedparser

def fetch_feed(url: str) -> dict:

    # Http Get + parse
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return feedparser.parse(response.content)
