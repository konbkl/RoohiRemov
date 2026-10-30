"""Core scanner: link filter + saare modules. Router sabse last me include hota hai."""
import asyncio
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton as B
from .. import checks, db
from ..logger import log_violation
from ..strings import t, sc
from ..utils import find_links, promo_mentions, member_status, mention, temp_reply, _del_later

router = Router()
TG_SERVICE = 777000
GROUP = F.chat.type.in_({"group", "supergroup"})
MEDIA = ("photo", "video", "document", "audio", "voice", "video_note", "sticker", "animation")

async def _violate(m: Message, lang: str, reason: str, detail: str, note="deleted_mod", kb=None, log=True) -> bool:
    try: await m.delete()
    except Exception: return True            # delete permission nahi -> aage mat badho
    await db.incr_stat("deleted")
    if log: await log_violation(m, reason.upper(), detail)
    await temp_reply(m, t(lang, note, user=mention(m), reason=reason), kb=kb)
    return True

async def process(m: Message, edited: bool):
    if m.is_automatic_forward: return
    if m.new_chat_members or m.left_chat_member or m.pinned_message or m.new_chat_title or m.new_chat_photo or m.delete_chat_photo: return
    if m.sender_chat and m.sender_chat.id == m.chat.id: return          # anonymous admin
    uid = m.from_user.id if m.from_user else None
    is_channel = bool(m.sender_chat) or uid == TG_SERVICE
    if uid and uid != TG_SERVICE:
        if str(uid) in await db.list_items("allowed", m.chat.id): return   # approved = sab filter se free
        if await member_status(m.bot, m.chat.id, uid) in ("creator", "administrator"): return

    g = await db.get_group(m.chat.id); lang = g["lang"]
    c = await db.cfg_all(m.chat.id)
    on = lambda k: c.get(k, "0") == "1"
    text = m.text or m.caption or ""
    low = text.lower()
    real_user = bool(uid and uid != TG_SERVICE)

    if edited and on("edit"):
        return await _violate(m, lang, "Edited message", "—")

    fs = c.get("fsub")                                                   # F-Sub
    if fs and real_user and not await checks.fsub_ok(m.bot, int(fs), uid):
        link = c.get("fsub_link")
        kb = InlineKeyboardMarkup(inline_keyboard=[[B(text=sc("Join channel"), url=link, style="success")]]) if link else None
        return await _violate(m, lang, "Force subscribe", fs, note="deleted_fsub", kb=kb)

    for w in await db.list_items("blacklist", m.chat.id):                # blacklist
        if w in low: return await _violate(m, lang, "Blacklist", w, note="deleted_bl")

    if text:
        if on("abuse"):
            hit = checks.abusive(text, await db.list_items("abuse", m.chat.id))
            if hit: return await _violate(m, lang, "Abuse", hit)
        if on("nsfw"):
            hit = checks.nsfw(text)
            if hit: return await _violate(m, lang, "NSFW", hit)
        if on("phone"):
            hit = checks.has_phone(text)
            if hit: return await _violate(m, lang, "Phone number", hit)
        if on("nohash"):
            hit = checks.has_hashtag(text)
            if hit: return await _violate(m, lang, "Hashtag", hit)
        if on("fonts"):
            hit = checks.stylish(text)
            if hit: return await _violate(m, lang, "Stylish font", hit)

    fwd = m.forward_origin
    if on("forward") and fwd: return await _violate(m, lang, "Forward", str(fwd.type))

    if on("promo"):
        hit = checks.promo_text(text) if text else None
        if not hit and fwd and fwd.type == "channel": hit = "forward from channel"
        if not hit and "@" in text:
            ms = await promo_mentions(m); hit = ", ".join(ms) if ms else None
        if hit: return await _violate(m, lang, "Promo", hit)

    if on("biomode") and real_user and await checks.bio_has_link(m.bot, uid):
        return await _violate(m, lang, "Bio link", "link in bio")

    # ---- link filter ----
    if is_channel: lon = g["block_channels"]
    elif m.from_user and m.from_user.is_bot: lon = g["block_bots"]
    else: lon = g["block_users"]
    if m.caption and not m.text and not g["block_captions"]: lon = 0
    if lon and text:
        links = find_links(m)
        if g["block_usernames"]: links += await promo_mentions(m)
        wl = await db.list_items("whitelist", m.chat.id)
        links = [l for l in links if not any(w in l.lower() for w in wl)]
        if links: return await _violate(m, lang, "Link", ", ".join(links), note="deleted")

    # ---- timed auto-delete (Msg-Del / Media-Del) ----
    sd, md = int(c.get("msgdel") or 0), int(c.get("mediadel") or 0)
    media = any(getattr(m, a, None) for a in MEDIA)
    delays = [x for x in (sd, md if media else 0) if x > 0]
    if delays: asyncio.create_task(_del_later(m, min(delays)))

@router.message(GROUP)
async def on_msg(m: Message): await process(m, False)

@router.edited_message(GROUP)
async def on_edit(m: Message): await process(m, True)
