import html
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from .. import db
from ..logger import log_setting
from ..strings import t
from ..utils import can_manage

router = Router()
G = F.chat.type.in_({"group", "supergroup"})

async def _guard(m: Message):
    lang = (await db.get_group(m.chat.id))["lang"]
    if not m.from_user or not await can_manage(m.bot, m.chat.id, m.from_user.id):
        await m.reply(t(lang, "no_perm")); return None
    return lang

def _target(m: Message, cmd: CommandObject):
    if m.reply_to_message and m.reply_to_message.from_user: return m.reply_to_message.from_user.id
    if cmd.args and cmd.args.strip().lstrip("-").isdigit(): return int(cmd.args.strip())

@router.message(Command("allow", "approve"), G)
async def allow(m: Message, command: CommandObject):
    lang = await _guard(m)
    if not lang: return
    uid = _target(m, command)
    if not uid: return await m.reply(t(lang, "need_target"))
    ok = await db.add_item("allowed", m.chat.id, uid)
    if ok: await log_setting(m.bot, m.chat, m.from_user, "User approved", uid)
    await m.reply(t(lang, "allowed_ok" if ok else "allowed_dup", user=f'<a href="tg://user?id={uid}">{uid}</a>'))

@router.message(Command("disallow", "unapprove"), G)
async def disallow(m: Message, command: CommandObject):
    lang = await _guard(m)
    if not lang: return
    uid = _target(m, command)
    if not uid: return await m.reply(t(lang, "need_target"))
    ok = await db.del_item("allowed", m.chat.id, uid)
    if ok: await log_setting(m.bot, m.chat, m.from_user, "User unapproved", uid)
    await m.reply(t(lang, "disallowed" if ok else "not_found"))

@router.message(Command("allowed", "approved"), G)
async def allowed(m: Message):
    lang = await _guard(m)
    if not lang: return
    items = await db.list_items("allowed", m.chat.id)
    body = "\n".join(f'• <a href="tg://user?id={i}">{i}</a>' for i in items) or t(lang, "empty")
    await m.reply(t(lang, "allowed_list", items=body))
