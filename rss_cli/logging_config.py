import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "rss_cli.log"

def setup_logging(level: int = logging.INFO) -> None:
    """
    Global configuration:
    - logs to console
    - logs to file logs/rss_cli.log
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
    )

    # Keep quiet several dll's
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
