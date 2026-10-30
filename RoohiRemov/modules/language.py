from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton as B
from .. import db
from ..strings import t, tp, LANGS, FLAGS
from ..logger import log_setting
from ..utils import can_manage, send_card, edit_card

router = Router()

async def picker(msg: Message, edit=False):
    cur = (await db.get_group(msg.chat.id))["lang"]
    btns = [B(text=("✔️ " if k == cur else FLAGS.get(k, "🌐") + " ") + v, callback_data=f"rr:l:{k}", **({"style": "success"} if k == cur else {})) for k, v in LANGS.items()]
    rows = [btns[i:i+2] for i in range(0, len(btns), 2)]
    rows.append([B(text=t(cur, "close"), callback_data="rr:close", style="danger"), B(text=t(cur, "back"), callback_data="rr:home", style="primary")])
    kb = InlineKeyboardMarkup(inline_keyboard=rows); text = t(cur, "lang_pick")
    await (edit_card(msg, text, kb) if edit else send_card(msg, text, kb))

@router.message(Command("language"))
async def language(m: Message):
    if m.chat.type != "private" and not await can_manage(m.bot, m.chat.id, m.from_user.id):
        return await m.reply(t((await db.get_group(m.chat.id))["lang"], "no_perm"))
    await picker(m)

@router.callback_query(F.data == "rr:lang")
async def lang_cb(c: CallbackQuery):
    await picker(c.message, edit=True); await c.answer()

@router.callback_query(F.data.startswith("rr:l:"))
async def set_lang(c: CallbackQuery):
    cid = c.message.chat.id
    if c.message.chat.type != "private" and not await can_manage(c.bot, cid, c.from_user.id):
        return await c.answer("Not allowed", show_alert=True)
    await db.set_group(cid, lang=c.data.split(":")[2])
    if c.message.chat.type != "private": await log_setting(c.bot, c.message.chat, c.from_user, "Language", c.data.split(":")[2])
    await picker(c.message, edit=True); await c.answer(tp(c.data.split(":")[2], "lang_set"))
