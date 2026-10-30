from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton as B
from .. import db
from ..logger import log_setting
from ..strings import t, tp, sc, MODNAMES
from ..utils import can_manage, member_status, send_card, edit_card

router = Router()
TOGGLES = [("block_users","t_users"),("block_bots","t_bots"),("block_channels","t_channels"),
           ("block_captions","t_captions"),("block_usernames","t_usernames")]

async def render(msg: Message, edit=False):
    g = await db.get_group(msg.chat.id); lang = g["lang"]
    st = lambda on: "success" if on else "danger"
    rows = [[B(text=f"{'✅' if g[c] else '❌'} {t(lang, k)}", callback_data=f"rr:tg:{c}", style=st(g[c]))] for c, k in TOGGLES]
    rows.append([B(text=f"{'✅' if g['admins_can_edit'] else '❌'} {t(lang,'t_admins')}", callback_data="rr:tg:admins_can_edit", style=st(g['admins_can_edit']))])
    rows.append([B(text=t(lang,"chlang"), callback_data="rr:lang", style="primary"), B(text=t(lang,"helpcmd"), callback_data="rr:help", style="primary")])
    rows.append([B(text=t(lang,"modules"), callback_data="rr:mods", style="success")])
    rows.append([B(text=t(lang,"close"), callback_data="rr:close", style="danger")])
    text = t(lang, "settings", au=await db.count_items("allowed", msg.chat.id),
             wl=await db.count_items("whitelist", msg.chat.id), bl=await db.count_items("blacklist", msg.chat.id))
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    await (edit_card(msg, text, kb) if edit else send_card(msg, text, kb))

@router.message(Command("settings"), F.chat.type == "private")
async def private_settings(m: Message):
    lang = (await db.get_group(m.chat.id))["lang"]
    await m.reply(t(lang, "groups_only"))

@router.message(Command("settings"), F.chat.type.in_({"group", "supergroup"}))
async def settings(m: Message):
    if not m.from_user or not await can_manage(m.bot, m.chat.id, m.from_user.id):
        return await m.reply(t((await db.get_group(m.chat.id))["lang"], "no_perm"))
    await render(m)

@router.callback_query(F.data.startswith("rr:tg:"))
async def toggle(c: CallbackQuery):
    chat_id, col = c.message.chat.id, c.data.split(":")[2]
    g = await db.get_group(chat_id)
    if col == "admins_can_edit":
        if await member_status(c.bot, chat_id, c.from_user.id) != "creator":
            return await c.answer("Only the group owner can change this.", show_alert=True)
    elif not await can_manage(c.bot, chat_id, c.from_user.id):
        return await c.answer(tp(g["lang"], "no_perm"), show_alert=True)
    await db.set_group(chat_id, **{col: 0 if g[col] else 1})
    await log_setting(c.bot, c.message.chat, c.from_user, col, "OFF" if g[col] else "ON")
    await render(c.message, edit=True); await c.answer()


# ---------------- Modules panel ----------------
BOOLS = ["phone", "promo", "nohash", "nsfw", "abuse", "biomode", "fonts", "forward", "edit", "autoapprove"]
DEFAULT_ON = {"autoapprove"}

async def render_modules(msg: Message, edit=False):
    lang = (await db.get_group(msg.chat.id))["lang"]; c = await db.cfg_all(msg.chat.id)
    rows, cur = [], []
    for k in BOOLS:
        on = c.get(k, "1" if k in DEFAULT_ON else "0") == "1"
        cur.append(B(text=f"{'✅' if on else '❌'} {sc(MODNAMES[k])}", callback_data=f"rr:m:{k}", style="success" if on else "danger"))
        if len(cur) == 2: rows.append(cur); cur = []
    if cur: rows.append(cur)
    rows.append([B(text=t(lang, "back"), callback_data="rr:home", style="primary"), B(text=t(lang, "close"), callback_data="rr:close", style="danger")])
    text = t(lang, "modules_title", md=c.get("mediadel", "0"), sd=c.get("msgdel", "0"), fs=c.get("fsub") or "—")
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    await (edit_card(msg, text, kb) if edit else send_card(msg, text, kb))

@router.callback_query(F.data == "rr:mods")
async def mods_cb(c: CallbackQuery):
    if not await can_manage(c.bot, c.message.chat.id, c.from_user.id):
        return await c.answer(tp((await db.get_group(c.message.chat.id))["lang"], "no_perm"), show_alert=True)
    await render_modules(c.message, edit=True); await c.answer()

@router.callback_query(F.data.startswith("rr:m:"))
async def mod_toggle(c: CallbackQuery):
    key, chat_id = c.data.split(":")[2], c.message.chat.id
    if key not in BOOLS: return await c.answer()
    if not await can_manage(c.bot, chat_id, c.from_user.id):
        return await c.answer(tp((await db.get_group(chat_id))["lang"], "no_perm"), show_alert=True)
    cur = (await db.cfg_all(chat_id)).get(key, "1" if key in DEFAULT_ON else "0")
    await db.cfg_set(chat_id, key, "0" if cur == "1" else "1")
    await log_setting(c.bot, c.message.chat, c.from_user, MODNAMES[key], "OFF" if cur == "1" else "ON")
    await render_modules(c.message, edit=True); await c.answer()
