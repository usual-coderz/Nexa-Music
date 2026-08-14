import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")

NEXA_API_URL = os.getenv("NEXA_API_URL", "https://api01.shrutibots.site")
NEXA_API_KEY = os.getenv("NEXA_API_KEY", "")

OWNER_ID = int(os.getenv("OWNER_ID", 0))
DOWNLOAD_DIR = "downloads"