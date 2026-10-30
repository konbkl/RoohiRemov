"""Owner-only (private chat): /stats /broadcast /live /autopromo"""
import asyncio
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from .. import config, db
from ..broadcast import blast, live_sender, state
from ..checks import parse_flags
from ..logger import card, send_log

router = Router()
OWN = (F.chat.type == "private") & (F.from_user.id == config.OWNER_ID)
STATS_F = (F.from_user.id == config.OWNER_ID) & ((F.chat.type == "private") | (F.chat.id == config.LOG_CHAT_ID))

@router.message(Command("stats"), STATS_F)
async def stats(m: Message):
    ch = await db.chats()
    users = sum(1 for c, _ in ch if c > 0); groups = sum(1 for c, _ in ch if c < 0)
    langs = {}
    for _, l in ch: langs[l] = langs.get(l, 0) + 1
    top = ", ".join(f"{k}: {v}" for k, v in sorted(langs.items(), key=lambda x: -x[1])[:5]) or "—"
    await m.reply(card("📊 Bot stats",
        ("👤 Users", f"<b>{users}</b>"), ("🏘 Groups & channels", f"<b>{groups}</b>"),
        ("💬 Total chats", f"<b>{users + groups}</b>"),
        ("🗑 Messages deleted", f"<b>{await db.get_stat('deleted')}</b>"),
        ("✅ Join requests approved", f"<b>{await db.get_stat('approved')}</b>"),
        ("🌐 Languages", top), ("🗄 Database", "MongoDB" if db.USE_MONGO else "SQLite")))

async def _run(m: Message, flag: str, fn, label: str):
    if state["busy"]: return await m.reply("⏳ A broadcast is already running.")
    status = await m.reply("📡 Broadcasting...")
    async def prog(i, n):
        try: await status.edit_text(f"📡 {i}/{n} done...")
        except Exception: pass
    res = await blast(m.bot, flag, fn, prog)
    if not res or res["total"] == 0:
        return await status.edit_text("No chats found for this target.")
    await status.edit_text(f"✅ Broadcast finished\n\nSent: <b>{res['ok']}</b>\nRemoved (dead chats): <b>{res['gone']}</b>\nFailed: <b>{res['fail']}</b>")
    await send_log(m.bot, card("📡 Broadcast finished", ("🎯 Target", flag), ("📝 Type", label), ("✅ Sent", str(res["ok"])),
                               ("🗑 Removed (dead)", str(res["gone"])), ("❌ Failed", str(res["fail"]))))

@router.message(Command("broadcast"), OWN)
async def broadcast(m: Message, command: CommandObject):
    flag, text = parse_flags(command.args)
    r = m.reply_to_message
    if r:
        async def fn(cid, lang): await m.bot.copy_message(cid, r.chat.id, r.message_id)
        label = "copied message"
    elif text:
        async def fn(cid, lang): await m.bot.send_message(cid, text)
        label = "text"
    else:
        return await m.reply("Usage:\n<code>/broadcast text</code> — everyone\n<code>/broadcast -user text</code> — users only\n"
                             "<code>/broadcast -group text</code> — groups &amp; channels only\nOr reply to a message with /broadcast.")
    asyncio.create_task(_run(m, flag, fn, label))

@router.message(Command("live"), OWN)
async def live(m: Message, command: CommandObject):
    flag, _ = parse_flags(command.args)
    me = await m.bot.get_me()
    asyncio.create_task(_run(m, flag, live_sender(m.bot, me.username), "launch post"))

@router.message(Command("autopromo"), OWN)
async def autopromo(m: Message, command: CommandObject):
    """/autopromo on|daily  -> roz  |  once -> sirf agle slot pe ek baar  |  off -> band"""
    arg = (command.args or "").strip().lower()
    if arg in ("on", "daily"): await db.cfg_set(0, "promo_on", "1"); await db.cfg_set(0, "promo_mode", "daily")
    elif arg == "once": await db.cfg_set(0, "promo_on", "1"); await db.cfg_set(0, "promo_mode", "once")
    elif arg == "off": await db.cfg_set(0, "promo_on", "0")
    c = await db.cfg_all(0)
    on = c.get("promo_on", "1" if config.AUTO_PROMO else "0") == "1"
    await m.reply(f"📅 Auto promo: <b>{'ON (' + c.get('promo_mode', 'daily') + ')' if on else 'OFF'}</b>\n"
                  f"🕒 Time: <b>{config.PROMO_AT} {config.PROMO_TZ}</b>\n📌 Last sent: <b>{c.get('promo_last') or '—'}</b>\n\n"
                  "<code>/autopromo daily</code> · <code>/autopromo once</code> · <code>/autopromo off</code>")
