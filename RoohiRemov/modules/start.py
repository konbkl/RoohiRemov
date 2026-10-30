import html
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from .. import config, db
from ..logger import log_new_user, log_event, chat_block, user_block
from ..strings import t, sc, MODNAMES, HELP_PAGES
from ..ui import btn, add_group_url, add_channel_url
from ..utils import send_card, edit_card

router = Router()

def _name(user):
    return f'<a href="tg://user?id={user.id}">{html.escape(user.first_name)}</a>' if user else "Admin"

async def welcome_text(bot, user, lang, key="welcome"):
    me = await bot.get_me()
    return t(lang, key, name=_name(user), bot=f'<a href="https://t.me/{me.username}">RoohiRemov</a>')

async def kb(bot, lang):
    me = await bot.get_me()
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn(t(lang, "add"), url=add_group_url(me.username))],
        [btn(t(lang, "addch"), url=add_channel_url(me.username))],
        [btn(t(lang, "owner"), url=config.OWNER_URL), btn(t(lang, "updates"), url=config.UPDATES_URL)],
        [btn(t(lang, "support"), url=config.SUPPORT_URL)],
        [btn(t(lang, "helpcmd"), callback_data="rr:help")],
        [btn(t(lang, "chlang"), callback_data="rr:lang")],
    ])

def page_kb(lang, p):
    names, rows = HELP_PAGES[p], []
    for i in range(0, len(names), 2):
        rows.append([btn(sc(MODNAMES[k]), callback_data=f"rr:hm:{k}") for k in names[i:i + 2]])
    nav = []
    if p > 0: nav.append(btn(t(lang, "prev"), callback_data=f"rr:hp:{p - 1}"))
    nav.append(btn(t(lang, "home") + " 🏡", callback_data="rr:home"))
    if p < len(HELP_PAGES) - 1: nav.append(btn(t(lang, "next"), callback_data=f"rr:hp:{p + 1}"))
    rows.append(nav)
    return InlineKeyboardMarkup(inline_keyboard=rows)

def module_kb(lang, key):
    p = next(i for i, pg in enumerate(HELP_PAGES) if key in pg)
    return InlineKeyboardMarkup(inline_keyboard=[[btn(t(lang, "prev"), callback_data=f"rr:hp:{p}"),
                                                  btn(t(lang, "home") + " 🏡", callback_data="rr:home")]])

@router.message(CommandStart(), F.chat.type == "private")
async def start(m: Message):
    lang = (await db.get_group(m.chat.id))["lang"]
    await send_card(m, await welcome_text(m.bot, m.from_user, lang), await kb(m.bot, lang), reply=True)
    await log_new_user(m)

@router.message(CommandStart(), F.chat.type.in_({"group", "supergroup"}))
async def start_group(m: Message):
    lang = (await db.get_group(m.chat.id))["lang"]
    me = await m.bot.get_me()
    k = InlineKeyboardMarkup(inline_keyboard=[
        [btn(t(lang, "add"), url=add_group_url(me.username))],
        [btn(t(lang, "helpcmd"), callback_data="rr:help"), btn(t(lang, "support"), url=config.SUPPORT_URL)]])
    await send_card(m, await welcome_text(m.bot, m.from_user, lang, "group_start"), k, reply=True)
    await log_event(m.bot, "▶️ /start used in a group", ("🏘 Group", chat_block(m.chat)), ("👤 By", user_block(m.from_user)))

@router.message(Command("help"))
async def help_(m: Message):
    lang = (await db.get_group(m.chat.id))["lang"]
    await send_card(m, t(lang, "help_main"), page_kb(lang, 0), reply=True)

@router.callback_query(F.data == "rr:help")
async def help_cb(c: CallbackQuery):
    lang = (await db.get_group(c.message.chat.id))["lang"]
    await edit_card(c.message, t(lang, "help_main"), page_kb(lang, 0)); await c.answer()

@router.callback_query(F.data.startswith("rr:hp:"))
async def help_page(c: CallbackQuery):
    lang = (await db.get_group(c.message.chat.id))["lang"]
    p = max(0, min(int(c.data.split(":")[2]), len(HELP_PAGES) - 1))
    await edit_card(c.message, t(lang, "help_main"), page_kb(lang, p)); await c.answer()

@router.callback_query(F.data.startswith("rr:hm:"))
async def help_module(c: CallbackQuery):
    lang = (await db.get_group(c.message.chat.id))["lang"]
    key = c.data.split(":")[2]
    if key not in MODNAMES: return await c.answer()
    await edit_card(c.message, t(lang, "h_" + key), module_kb(lang, key)); await c.answer()

@router.callback_query(F.data == "rr:home")
async def home_cb(c: CallbackQuery):
    lang = (await db.get_group(c.message.chat.id))["lang"]
    if c.message.chat.type == "private":
        await edit_card(c.message, await welcome_text(c.bot, c.from_user, lang), await kb(c.bot, lang))
    else:
        from .settings import render
        await render(c.message, edit=True)
    await c.answer()

@router.callback_query(F.data == "rr:close")
async def close_cb(c: CallbackQuery):
    try: await c.message.delete()
    except Exception: pass
