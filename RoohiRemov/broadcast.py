"""Broadcast engine (owner commands + auto promo dono yahi use karte hain)."""
import asyncio, os
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from aiogram.types import FSInputFile
from . import config, db
from .strings import t
from .ui import promo_kb

DEAD = ("blocked", "kicked", "chat not found", "deactivated", "not a member", "user not found", "group chat was deleted")
state = {"busy": False}
_cache: dict[str, str] = {}

async def _try(fn, cid, lang) -> str:
    for _ in range(3):
        try:
            await fn(cid, lang); return "ok"
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
        except Exception as e:
            if any(x in str(e).lower() for x in DEAD):
                await db.remove_chat(cid); return "gone"
            return "fail"
    return "fail"

async def blast(bot, flag: str, fn, progress=None):
    """Returns dict(ok, gone, fail, total) ya None agar koi aur broadcast chal raha ho."""
    if state["busy"]: return None
    chats = [(c, l) for c, l in await db.chats() if flag == "all" or (flag == "user" and c > 0) or (flag == "group" and c < 0)]
    res = {"ok": 0, "gone": 0, "fail": 0, "total": len(chats)}
    if not chats: return res
    state["busy"] = True
    try:
        for i, (cid, lang) in enumerate(chats, 1):
            res[await _try(fn, cid, lang)] += 1
            if progress and i % 100 == 0: await progress(i, len(chats))
            await asyncio.sleep(0.05)
    finally:
        state["busy"] = False
    return res

def _promo_media():
    if _cache.get("fid"): return _cache["fid"]
    p = config.PROMO_IMG
    if p and os.path.isfile(p): return FSInputFile(p)
    return p if p else config.START_IMG

def live_sender(bot, username: str):
    """Launch post: promo image + text + Add buttons (har chat ki language me)."""
    async def fn(cid, lang):
        text, kb, media = t(lang, "live"), promo_kb(username, lang), _promo_media()
        if media:
            try:
                sent = await bot.send_photo(cid, media, caption=text, reply_markup=kb)
                if sent.photo: _cache["fid"] = sent.photo[-1].file_id
                return
            except TelegramBadRequest:
                pass
        await bot.send_message(cid, text, reply_markup=kb)
    return fn
