import os
from dotenv import load_dotenv
from pathlib import Path

### Loader .env
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(env_path)

### Variable config
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587")) # Protocols: 587(TLS), 465(SSL)
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

### Message
MSG_SUBJECT = os.getenv("MSG_SUBJECT")
MSG_ADDRESS = os.getenv("MSG_ADDRESS")

### API
API_GROQ_KEY = os.getenv("API_GROQ_KEY")

### Init import object
config_file = (BASE_DIR, env_path)
config_smtp = (SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD)
config_message = (MSG_SUBJECT, MSG_ADDRESS)

### Additional
# DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "10"))
# LOGGING_ENABLED = os.getenv("LOGGING_ENABLED", "true").lower() == "true"