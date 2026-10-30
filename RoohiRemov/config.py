import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
BOT_TOKEN = os.environ["BOT_TOKEN"]
OWNER_ID = int(os.getenv("OWNER_ID") or 0)
UPDATES_URL = os.getenv("UPDATES_URL", "https://t.me/telegram")
SUPPORT_URL = os.getenv("SUPPORT_URL", "https://t.me/telegram")
DB_PATH = os.getenv("DB_PATH", "roohiremov.db")
MONGO_URI = os.getenv("MONGO_URI") or None
MONGO_DB = os.getenv("MONGO_DB", "roohiremov")
LOG_CHAT_ID = int(os.getenv("LOG_CHAT_ID") or 0)
PING_IMG = os.getenv("PING_IMG", "https://files.catbox.moe/1egfqy.png")
START_IMG = os.getenv("START_IMG") or PING_IMG   # /start, /ping, help, broadcast post: ye image
PREMIUM_EMOJI = os.getenv("PREMIUM_EMOJI", "false").lower() == "true"

OWNER_URL = os.getenv("OWNER_URL") or (f"tg://user?id={OWNER_ID}" if OWNER_ID else "https://t.me/telegram")

# ---- Auto promo (daily live post) ----
_ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "promo.png")
PROMO_IMG = os.getenv("PROMO_IMG") or _ASSETS          # local file ya URL/file_id
AUTO_PROMO = os.getenv("AUTO_PROMO", "true").lower() == "true"
PROMO_AT = os.getenv("PROMO_AT", "07:00")              # HH:MM (24h)
PROMO_TZ = os.getenv("PROMO_TZ", "Asia/Kolkata")
