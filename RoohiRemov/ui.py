"""Buttons: random colours + Add-me links (saari permissions ke saath)."""
import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B
from . import config
from .strings import t

def rc() -> str:
    return random.choice(("primary", "success", "danger"))      # blue / green / red

def btn(text, style=None, **kw):
    return B(text=text, style=style or rc(), **kw)

def add_group_url(username: str) -> str:
    return f"https://t.me/{username}?startgroup=true&admin=delete_messages+invite_users+restrict_members"

def add_channel_url(username: str) -> str:
    return f"https://t.me/{username}?startchannel=true&admin=invite_users+post_messages"

def promo_kb(username: str, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn(t(lang, "add"), url=add_group_url(username))],
        [btn(t(lang, "addch"), url=add_channel_url(username))],
        [btn(t(lang, "updates"), url=config.UPDATES_URL), btn(t(lang, "support"), url=config.SUPPORT_URL)]])
