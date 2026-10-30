"""Module commands: /phone /promo /nohash /nsfw /abuse /biomode /fonts /forward /edit /autoapprove
/mediadel /msgdel /fsub /addabuse /rmabuse /abusewords /echo /purge + auto-approve join requests."""
import html
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton as B
from .. import db
from ..logger import log, log_setting, log_event, chat_block, user_block
from ..strings import t, MODNAMES
from ..utils import can_manage, temp_reply

router = Router()
G = F.chat.type.in_({"group", "supergroup"})
BOOL = {"phone": ("phone",), "promo": ("promo",), "nohash": ("nohash", "hashtag"), "nsfw": ("nsfw",),
        "abuse": ("abuse",), "biomode": ("biomode", "bio"), "fonts": ("fonts",), "forward": ("forward",),
        "edit": ("edit",), "autoapprove": ("autoapprove",)}
DEFAULT_ON = {"autoapprove"}

async def _perm(m: Message):
    lang = (await db.get_group(m.chat.id))["lang"]
    if m.chat.type == "channel": return lang            # channel me sirf admins post kar sakte hain
    if not m.from_user or not await can_manage(m.bot, m.chat.id, m.from_user.id):
        await m.reply(t(lang, "no_perm")); return None
    return lang

def _bool(key):
    async def h(m: Message, command: CommandObject):
        lang = await _perm(m)
        if not lang: return
        cur = (await db.cfg_all(m.chat.id)).get(key, "1" if key in DEFAULT_ON else "0")
        arg = (command.args or "").strip().lower()
        if arg in ("on", "yes", "enable", "off", "no", "disable"):
            cur = "1" if arg in ("on", "yes", "enable") else "0"
            await db.cfg_set(m.chat.id, key, cur)
            await log_setting(m.bot, m.chat, m.from_user, MODNAMES[key], "ON" if cur == "1" else "OFF")
        await m.reply(t(lang, "mod_on" if cur == "1" else "mod_off", mod=MODNAMES[key], cmd=command.command))
    return h

for _k, _names in BOOL.items():
    router.message.register(_bool(_k), Command(*_names), G)
router.channel_post.register(_bool("autoapprove"), Command("autoapprove"))

def _timed(key):
    async def h(m: Message, command: CommandObject):
        lang = await _perm(m)
        if not lang: return
        arg = (command.args or "").strip().lower()
        if arg in ("off", "0", "no"):
            await db.cfg_set(m.chat.id, key, 0); await log_setting(m.bot, m.chat, m.from_user, MODNAMES[key], "OFF"); return await m.reply(t(lang, "timed_off", mod=MODNAMES[key]))
        if arg.isdigit() and 5 <= int(arg) <= 86400:
            await db.cfg_set(m.chat.id, key, int(arg)); await log_setting(m.bot, m.chat, m.from_user, MODNAMES[key], f"{int(arg)}s"); return await m.reply(t(lang, "timed_set", mod=MODNAMES[key], n=int(arg)))
        cur = (await db.cfg_all(m.chat.id)).get(key) or 0
        await m.reply(t(lang, "timed_usage", mod=MODNAMES[key], cur=cur, cmd=command.command))
    return h
router.message.register(_timed("mediadel"), Command("mediadel"), G)
router.message.register(_timed("msgdel"), Command("msgdel"), G)

@router.message(Command("fsub"), G)
async def fsub(m: Message, command: CommandObject):
    lang = await _perm(m)
    if not lang: return
    arg = (command.args or "").strip()
    if not arg: return await m.reply(t(lang, "fsub_show", cur=(await db.cfg_all(m.chat.id)).get("fsub") or "off"))
    if arg.lower() in ("off", "0", "no"):
        await db.cfg_set(m.chat.id, "fsub", ""); await db.cfg_set(m.chat.id, "fsub_link", "")
        await log_setting(m.bot, m.chat, m.from_user, "F-Sub", "OFF")
        return await m.reply(t(lang, "fsub_off"))
    ref = arg if arg.startswith("@") else (int(arg) if arg.lstrip("-").isdigit() else None)
    if ref is None: return await m.reply(t(lang, "fsub_bad"))
    try:
        chan = await m.bot.get_chat(ref)
        me = await m.bot.get_chat_member(chan.id, (await m.bot.get_me()).id)
        if me.status not in ("administrator", "creator"): raise ValueError("not admin")
    except Exception:
        return await m.reply(t(lang, "fsub_need_admin"))
    link = f"https://t.me/{chan.username}" if chan.username else ""
    if not link:
        try: link = await m.bot.export_chat_invite_link(chan.id)
        except Exception: link = ""
    await db.cfg_set(m.chat.id, "fsub", chan.id); await db.cfg_set(m.chat.id, "fsub_link", link)
    await log_setting(m.bot, m.chat, m.from_user, "F-Sub", f"{chan.title} ({chan.id})")
    await m.reply(t(lang, "fsub_set", chan=html.escape(chan.title or str(chan.id))))

@router.message(Command("addabuse"), G)
async def addabuse(m: Message, command: CommandObject):
    lang = await _perm(m)
    if not lang: return
    if not command.args: return await m.reply(t(lang, "abuse_usage"))
    await db.add_item("abuse", m.chat.id, command.args.strip().lower()); await log_setting(m.bot, m.chat, m.from_user, "Abuse word added", command.args.strip()); await m.reply(t(lang, "abuse_ok"))

@router.message(Command("rmabuse"), G)
async def rmabuse(m: Message, command: CommandObject):
    lang = await _perm(m)
    if not lang: return
    if not command.args: return await m.reply(t(lang, "abuse_usage"))
    ok = await db.del_item("abuse", m.chat.id, command.args.strip().lower())
    if ok: await log_setting(m.bot, m.chat, m.from_user, "Abuse word removed", command.args.strip())
    await m.reply(t(lang, "abuse_rm" if ok else "not_found"))

@router.message(Command("abusewords"), G)
async def abusewords(m: Message):
    lang = (await db.get_group(m.chat.id))["lang"]
    items = await db.list_items("abuse", m.chat.id)
    await m.reply(t(lang, "abuse_list", items="\n".join(f"• {html.escape(i)}" for i in items) or t(lang, "empty")))

@router.message(Command("echo"), G)
async def echo(m: Message, command: CommandObject):
    lang = await _perm(m)
    if not lang: return
    r = m.reply_to_message
    if command.args: await m.answer(html.escape(command.args))
    elif r: await m.bot.copy_message(m.chat.id, m.chat.id, r.message_id)
    else: return await m.reply(t(lang, "echo_usage"))
    await log_event(m.bot, "📣 Echo used", ("🏘 Chat", chat_block(m.chat)), ("👤 By", user_block(m.from_user)))
    try: await m.delete()
    except Exception: pass

@router.message(Command("purge"), G)
async def purge(m: Message):
    lang = await _perm(m)
    if not lang: return
    if not m.reply_to_message: return await m.reply(t(lang, "purge_usage"))
    ids = list(range(m.reply_to_message.message_id, m.message_id + 1))[:1000]
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        try: await m.bot.delete_messages(m.chat.id, chunk)
        except Exception:
            for mid in chunk:
                try: await m.bot.delete_message(m.chat.id, mid)
                except Exception: pass
    await log_event(m.bot, "🧹 Purge", ("🏘 Chat", chat_block(m.chat)), ("👤 By", user_block(m.from_user)), ("🗑 Messages", str(len(ids))))
    await temp_reply(m, t(lang, "purge_done", n=len(ids)))

@router.chat_join_request()
async def join_request(r: ChatJoinRequest):
    """Groups + channels: join request auto-approve (default ON)."""
    g = await db.get_group(r.chat.id)
    if (await db.cfg_all(r.chat.id)).get("autoapprove", "1") != "1": return
    try: await r.approve()
    except Exception as ex:
        return log.warning("approve fail %s: %s", r.chat.id, ex)
    await db.incr_stat("approved")
    await log_event(r.bot, "✅ Join request approved", ("🏘 Chat", chat_block(r.chat)), ("👤 User", user_block(r.from_user)))
    me = await r.bot.get_me()
    kb = InlineKeyboardMarkup(inline_keyboard=[[B(text=t(g["lang"], "add"), style="success",
          url=f"https://t.me/{me.username}?startgroup=true&admin=delete_messages")]])
    try:
        await r.bot.send_message(r.user_chat_id, t(g["lang"], "approved_dm",
                                 name=html.escape(r.from_user.first_name), chat=html.escape(r.chat.title or "")), reply_markup=kb)
    except Exception: pass
