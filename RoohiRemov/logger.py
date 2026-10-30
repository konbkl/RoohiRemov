"""Logger: important events only (deletes, add/remove, start, settings, errors). Never logs every message."""
import datetime, html, logging, os
from logging.handlers import RotatingFileHandler
from aiogram import Bot
from aiogram.types import Message, LinkPreviewOptions, InlineKeyboardMarkup, InlineKeyboardButton as B
from . import config
from .strings import sc

log = logging.getLogger("roohiremov")
_case = 0   # chalte waqt ka case counter

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                        handlers=[logging.StreamHandler(),
                                  RotatingFileHandler("logs/roohiremov.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8")])

def now() -> str:
    return datetime.datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

def user_block(u) -> str:
    if not u: return "—"
    un = f" (@{u.username})" if u.username else ""
    return f'<a href="tg://user?id={u.id}">{html.escape(u.full_name)}</a>{un}\n🆔 <code>{u.id}</code>'

def chat_block(c) -> str:
    un = f" (@{c.username})" if getattr(c, "username", None) else ""
    return f"{html.escape(c.title or c.full_name or '?')}{un}\n🆔 <code>{c.id}</code>"

def card(title: str, *rows: tuple[str, str]) -> str:
    """Blockquote card: title + (label, value) rows. Labels pe font lagta hai."""
    body = "\n".join(f"{sc(lab)}: {val}" for lab, val in rows)
    return f"<b>{sc(title)}</b>\n<blockquote>{body}</blockquote>\n🕒 <code>{now()}</code>"

async def send_log(bot: Bot, text: str, kb: InlineKeyboardMarkup | None = None):
    log.info(text.replace("\n", " | ")[:300])
    if not config.LOG_CHAT_ID: return
    try:
        await bot.send_message(config.LOG_CHAT_ID, text[:4000], reply_markup=kb,
                               link_preview_options=LinkPreviewOptions(is_disabled=True))
    except Exception as ex:
        log.warning("could not send to log chat: %s", ex)

def group_btn(chat) -> list:
    return [B(text=sc("Open group"), url=f"https://t.me/{chat.username}")] if getattr(chat, "username", None) else []

async def log_event(bot: Bot, title: str, *rows: tuple[str, str]):
    await send_log(bot, card(title, *rows))

async def log_setting(bot: Bot, chat, user, what: str, value):
    await send_log(bot, card("⚙️ Setting changed", ("🏘 Chat", chat_block(chat)), ("👤 By", user_block(user)),
                             ("🧩 Setting", html.escape(str(what))), ("✏️ Value", html.escape(str(value)))))

async def log_startup(bot: Bot):
    me = await bot.get_me()
    await send_log(bot, card("🚀 Bot started", ("🤖 Bot", f"@{me.username}\n🆔 <code>{me.id}</code>")))

async def log_shutdown(bot: Bot):
    await send_log(bot, card("🛑 Bot stopped"))

async def log_new_user(m: Message):
    await send_log(m.bot, card("👤 New user started bot", ("👤 User", user_block(m.from_user))))

async def log_violation(m: Message, reason: str, detail: str):
    """Sirf jab bot koi message DELETE kare."""
    global _case; _case += 1
    u = m.from_user
    shown = (m.text or m.caption or f"<{m.content_type}>")[:300]
    who = user_block(u) if u else chat_block(m.sender_chat)
    rows = [("🏘 Group", chat_block(m.chat)), ("👤 User", who), ("📌 Reason", reason),
            ("🔎 Detected", f"<code>{html.escape(detail[:200])}</code>"),
            ("💬 Message", f"<code>{html.escape(shown)}</code>")]
    kb_rows = []
    if u and not u.is_bot:
        kb_rows.append([B(text=sc("✅ Allow user"), callback_data=f"lg:a:{m.chat.id}:{u.id}", style="success"),
                        B(text=sc("🚫 Ban user"), callback_data=f"lg:b:{m.chat.id}:{u.id}", style="danger")])
    if group_btn(m.chat): kb_rows.append(group_btn(m.chat))
    await send_log(m.bot, card(f"🗑 Message deleted • #{_case}", *rows),
                   InlineKeyboardMarkup(inline_keyboard=kb_rows) if kb_rows else None)
