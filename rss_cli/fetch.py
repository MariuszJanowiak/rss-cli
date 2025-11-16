import requests
import feedparser
from decorators import timer, retry, rate_limit

@rate_limit(5, 2)
@retry((requests.exceptions.RequestException,), tries=3, delay=1)
@timer
def fetch_feed(url: str) -> dict:

    # Http Get + parse
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return feedparser.parse(response.content)