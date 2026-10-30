import html
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from .. import db
from ..strings import t
from ..utils import can_manage

router = Router()
G = F.chat.type.in_({"group", "supergroup"})

async def _guard(m):
    lang = (await db.get_group(m.chat.id))["lang"]
    if not m.from_user or not await can_manage(m.bot, m.chat.id, m.from_user.id):
        await m.reply(t(lang, "no_perm")); return None
    return lang

@router.message(Command("blacklist"), G)
async def blacklist(m: Message, command: CommandObject):
    lang = await _guard(m)
    if not lang: return
    text = command.args or (m.reply_to_message.text or m.reply_to_message.caption if m.reply_to_message else None)
    if not text: return await m.reply(t(lang, "bl_usage"))
    await db.add_item("blacklist", m.chat.id, text.strip().lower())
    await m.reply(t(lang, "bl_ok"))

@router.message(Command("rblacklist"), G)
async def rblacklist(m: Message, command: CommandObject):
    lang = await _guard(m)
    if not lang: return
    if not command.args: return await m.reply(t(lang, "bl_usage"))
    arg, items = command.args.strip().lower(), await db.list_items("blacklist", m.chat.id)
    if arg.isdigit() and 1 <= int(arg) <= len(items): arg = items[int(arg) - 1]
    ok = await db.del_item("blacklist", m.chat.id, arg)
    await m.reply(t(lang, "bl_rm" if ok else "not_found"))

@router.message(Command("blacklisted"), G)
async def blacklisted(m: Message):
    lang = (await db.get_group(m.chat.id))["lang"]
    items = await db.list_items("blacklist", m.chat.id)
    body = "\n".join(f"{i}. {html.escape(x)}" for i, x in enumerate(items, 1)) or t(lang, "empty")
    await m.reply(t(lang, "bl_list", items=body))
