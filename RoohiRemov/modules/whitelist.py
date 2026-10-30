import html
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from .. import db
from ..strings import t
from ..utils import can_manage

router = Router()
G = F.chat.type.in_({"group", "supergroup"})

def norm(u: str) -> str:
    u = u.strip().lower()
    for p in ("https://", "http://", "www."):
        if u.startswith(p): u = u[len(p):]
    return u.rstrip("/")

@router.message(Command("whitelist"), G)
async def whitelist(m: Message, command: CommandObject):
    lang = (await db.get_group(m.chat.id))["lang"]
    if not command.args:
        items = await db.list_items("whitelist", m.chat.id)
        body = "\n".join(f"• {html.escape(i)}" for i in items) or t(lang, "empty")
        return await m.reply(t(lang, "wl_list", items=body))
    if not m.from_user or not await can_manage(m.bot, m.chat.id, m.from_user.id):
        return await m.reply(t(lang, "no_perm"))
    if await db.count_items("whitelist", m.chat.id) >= 10:
        return await m.reply(t(lang, "wl_max"))
    await db.add_item("whitelist", m.chat.id, norm(command.args.split()[0]))
    await m.reply(t(lang, "wl_ok"))

@router.message(Command("rwhitelist"), G)
async def rwhitelist(m: Message, command: CommandObject):
    lang = (await db.get_group(m.chat.id))["lang"]
    if not m.from_user or not await can_manage(m.bot, m.chat.id, m.from_user.id):
        return await m.reply(t(lang, "no_perm"))
    if not command.args: return await m.reply(t(lang, "wl_usage"))
    ok = await db.del_item("whitelist", m.chat.id, norm(command.args.split()[0]))
    await m.reply(t(lang, "wl_rm" if ok else "not_found"))
