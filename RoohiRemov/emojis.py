"""Premium (custom) emoji map.
Har naam: (fallback normal emoji, custom_emoji_id).
custom_emoji_id apne emoji pack se lo (@GetEmojiIDbot / @idstickerbot ko premium emoji bhejo)
aur neeche ID_HERE ki jagah paste karo."""
from . import config

EMOJI = {
    "rocket":  ("🚀", "ID_HERE"),
    "diamond": ("🔹", "ID_HERE"),
    "heart":   ("💖", "ID_HERE"),
    "shield":  ("🛡", "ID_HERE"),
    "gear":    ("⚙️", "ID_HERE"),
    "warn":    ("⚠️", "ID_HERE"),
    "crown":   ("👑", "ID_HERE"),
    "user":    ("👤", "ID_HERE"),
    "ban":     ("🚫", "ID_HERE"),
    "tick":    ("✅", "ID_HERE"),
    "globe":   ("🌐", "ID_HERE"),
    "cross":   ("❌", "ID_HERE"),
    "bell":    ("📢", "ID_HERE"),
    "help":    ("💡", "ID_HERE"),
}

def e(name: str) -> str:
    fb, cid = EMOJI[name]
    if config.PREMIUM_EMOJI and cid != "ID_HERE":
        return f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>'
    return fb
