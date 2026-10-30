"""Pure filter helpers (no aiogram import) — remover.py inhe use karta hai."""
import re, time

URL_RE = re.compile(
    r"(https?://\S+|www\.\S+|\b(?:t\.me|telegram\.me|telegram\.dog)/\S+|"
    r"\b[a-z0-9-]+\.(?:com|net|org|in|io|me|xyz|co|info|link|site|online|app|dev|tk|ml|ga|cf|gg|ly|to|cc|tv|club|top|live|shop|store|bio)\b\S*)", re.I)
PHONE_RE = re.compile(r"(?<!\w)\+?\d[\d\s\-().]{8,}\d(?!\w)")
HASH_RE = re.compile(r"(?<!\w)#\w+", re.U)
PROMO_RE = re.compile(r"(?<!\w)(paid\s+promo(?:tion)?|promotion|promo|dm\s+(?:me\s+)?for|join\s+(?:my|our|us)|"
                      r"subscribe|follow\s+(?:me|us)|collab(?:oration)?|giveaway|earn\s+money|referral|work\s+from\s+home)(?!\w)", re.I)

NSFW_WORDS = ["porn", "pornhub", "xxx", "nude", "nudes", "naked", "onlyfans", "hentai", "blowjob", "handjob",
              "sex video", "sex chat", "sexchat", "adult video", "18+", "nsfw", "boobs", "pussy", "dick pic",
              "cam girl", "call girl", "escort", "randi", "bf video", "desi mms", "mms video"]
ABUSE_WORDS = ["madarchod", "behenchod", "bhenchod", "chutiya", "gandu", "bhosdike", "bsdk", "randi", "lund",
               "loda", "mc", "bc", "fuck", "fucker", "motherfucker", "bitch", "asshole", "bastard", "dick",
               "pussy", "slut", "whore"]

def _words_re(words) -> re.Pattern:
    ws = sorted({w for w in words if w}, key=len, reverse=True)
    return re.compile(r"(?<!\w)(?:" + "|".join(re.escape(w) for w in ws) + r")(?!\w)", re.I)

_NSFW = _words_re(NSFW_WORDS)
_ABUSE = _words_re(ABUSE_WORDS)
_STYLE = set("ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡʏᴢΛΣεση")

def has_phone(text: str):
    for mt in PHONE_RE.finditer(text):
        if 10 <= len(re.sub(r"\D", "", mt.group(0))) <= 15: return mt.group(0)

def has_hashtag(text: str):
    mt = HASH_RE.search(text); return mt.group(0) if mt else None

def nsfw(text: str):
    mt = _NSFW.search(text); return mt.group(0) if mt else None

def abusive(text: str, custom=()):
    mt = _ABUSE.search(text)
    if mt: return mt.group(0)
    if custom:
        mt = _words_re(custom).search(text); return mt.group(0) if mt else None

def promo_text(text: str):
    mt = PROMO_RE.search(text); return mt.group(0) if mt else None

def stylish(text: str):
    """Fancy unicode fonts (math bold/italic, fullwidth, circled, small caps...) — 3+ chars => True"""
    hits = []
    for ch in text:
        o = ord(ch)
        if (0x1D400 <= o <= 0x1D7FF or 0xFF21 <= o <= 0xFF5A or 0x24B6 <= o <= 0x24E9 or
                0x1F130 <= o <= 0x1F189 or 0x2100 <= o <= 0x214F or ch in _STYLE):
            hits.append(ch)
            if len(hits) >= 3: return "".join(hits)

_bio_cache: dict[int, tuple[float, bool]] = {}
async def bio_has_link(bot, uid: int) -> bool:
    hit = _bio_cache.get(uid)
    if hit and time.time() - hit[0] < 600: return hit[1]
    try: bio = (await bot.get_chat(uid)).bio or ""
    except Exception: bio = ""
    bad = bool(URL_RE.search(bio))
    _bio_cache[uid] = (time.time(), bad); return bad

_fsub_cache: dict[tuple[int, int], float] = {}
async def fsub_ok(bot, chan: int, uid: int) -> bool:
    ts = _fsub_cache.get((chan, uid))
    if ts and time.time() - ts < 120: return True
    try: st = (await bot.get_chat_member(chan, uid)).status
    except Exception: return True          # check nahi ho paya -> block mat karo
    ok = st not in ("left", "kicked")
    if ok: _fsub_cache[(chan, uid)] = time.time()
    return ok


# ---------- small pure helpers ----------
_FLAGS = {"-user": "user", "-users": "user", "-group": "group", "-groups": "group", "-all": "all"}

def parse_flags(args):
    """'/broadcast -user hello' -> ('user', 'hello'). Default target = all."""
    text = (args or "").strip(); flag = "all"
    parts = text.split(None, 1)
    if parts and parts[0].lower() in _FLAGS:
        flag = _FLAGS[parts[0].lower()]; text = parts[1].strip() if len(parts) > 1 else ""
    return flag, text

def fmt_uptime(sec: float) -> str:
    sec = int(sec); d, sec = divmod(sec, 86400); h, sec = divmod(sec, 3600); m, s = divmod(sec, 60)
    return " ".join(x for x in (f"{d}d" if d else "", f"{h}h" if h else "", f"{m}m" if m else "", f"{s}s") if x)

def is_due(now, hh: int, mm: int, last: str, window_hours: float = 3) -> bool:
    """Aaj ka scheduled time nikal gaya, 3 ghante ke andar hai, aur aaj abhi tak bheja nahi."""
    due = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    return now >= due and (now - due).total_seconds() < window_hours * 3600 and last != now.strftime("%Y-%m-%d")
