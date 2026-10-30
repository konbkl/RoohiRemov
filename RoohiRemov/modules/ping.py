"""/ping — latency + uptime + banner image."""
import time
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup
from .. import db
from ..checks import fmt_uptime
from ..strings import t
from ..ui import btn, add_group_url
from ..utils import send_card

router = Router()
BOOT = time.time()

@router.message(Command("ping"))
async def ping(m: Message):
    lang = (await db.get_group(m.chat.id))["lang"]
    t0 = time.perf_counter(); me = await m.bot.get_me(); ms = (time.perf_counter() - t0) * 1000
    botl = f'<a href="https://t.me/{me.username}">@{me.username}</a>'
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn(t(lang, "add"), url=add_group_url(me.username))]])
    await send_card(m, t(lang, "ping", ms=f"{ms:.1f}", up=fmt_uptime(time.time() - BOOT), bot=botl), kb, reply=True)
