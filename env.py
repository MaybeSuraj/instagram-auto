import os
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


API_ID = int(_require_env("API_ID"))
API_HASH = _require_env("API_HASH")
BOT_TOKEN = _require_env("BOT_TOKEN")
INSTAGRAM_SESSION_ID = _require_env("INSTAGRAM_SESSION_ID")
OWNER_ID = int(_require_env("OWNER_ID"))


owner_filter = filters.user(OWNER_ID)
