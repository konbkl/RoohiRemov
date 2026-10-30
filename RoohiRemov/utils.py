import asyncio, re, html
from aiogram import Bot
from aiogram.types import Message
from . import db

from .checks import URL_RE

async def member_status(bot: Bot, chat_id: int, uid: int) -> str:
    try: return (await bot.get_chat_member(chat_id, uid)).status
    except Exception: return "left"

async def can_manage(bot: Bot, chat_id: int, uid: int) -> bool:
    s = await member_status(bot, chat_id, uid)
    if s == "creator": return True
    if s == "administrator": return bool((await db.get_group(chat_id))["admins_can_edit"])
    return False

def mention(m: Message) -> str:
    u = m.from_user
    if not u: return html.escape(m.sender_chat.title if m.sender_chat else "User")
    return f'<a href="tg://user?id={u.id}">{html.escape(u.first_name)}</a>'

async def _del_later(msg: Message, secs: int):
    await asyncio.sleep(secs)
    try: await msg.delete()
    except Exception: pass

async def temp_reply(m: Message, text: str, secs: int = 10, kb=None):
    sent = await m.answer(text, reply_markup=kb)
    asyncio.create_task(_del_later(sent, secs))

def find_links(m: Message, count_usernames: bool = False) -> list[str]:
    text = m.text or m.caption or ""
    ents = m.entities or m.caption_entities or []
    found = []
    for en in ents:
        if en.type == "url": found.append(en.extract_from(text))
        elif en.type == "text_link" and en.url: found.append(en.url)
    found += [x.group(0) for x in URL_RE.finditer(text)]
    return list(dict.fromkeys(found))

# ---------- card helpers (banner photo ke saath/bina) ----------
from aiogram.exceptions import TelegramBadRequest
from . import config

_fid = None   # pehli successful send ke baad image ka file_id cache

async def send_card(msg: Message, text: str, kb=None, reply=False):
    global _fid
    img = _fid or config.START_IMG
    if img and len(text) <= 1000:
        f = msg.reply_photo if reply else msg.answer_photo
        try:
            sent = await f(img, caption=text, reply_markup=kb)
            if sent.photo: _fid = sent.photo[-1].file_id
            return sent
        except TelegramBadRequest:
            pass                                   # image/caption problem -> text fallback
    return await (msg.reply if reply else msg.answer)(text, reply_markup=kb)

async def edit_card(msg: Message, text: str, kb=None):
    try:
        if msg.photo and len(text) > 1000:        # caption limit -> photo hata ke text bhejo
            await msg.delete(); await msg.answer(text, reply_markup=kb)
        elif msg.photo: await msg.edit_caption(caption=text, reply_markup=kb)
        else: await msg.edit_text(text, reply_markup=kb)
    except TelegramBadRequest:
        pass  # "message is not modified" etc.


# ---------- @username: sirf channel/group promo block, normal users/bots NAHI ----------
_mention_cache: dict[str, bool] = {}

async def is_promo_username(bot: Bot, uname: str) -> bool:
    key = uname.lower()
    if key in _mention_cache: return _mention_cache[key]
    try:
        chat = await bot.get_chat(uname)
        bad = chat.type in ("channel", "group", "supergroup")
    except Exception:
        bad = False          # user/bot ya nahi mila -> allow
    _mention_cache[key] = bad
    return bad

async def promo_mentions(m: Message) -> list[str]:
    text = m.text or m.caption or ""
    out = []
    for en in (m.entities or m.caption_entities or []):
        if en.type == "mention":
            un = en.extract_from(text)
            if await is_promo_username(m.bot, un): out.append(un)
    return out
