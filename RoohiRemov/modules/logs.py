"""Bot add/remove/admin events + log card ke Allow/Ban buttons."""
from aiogram import Router, F
from aiogram.types import ChatMemberUpdated, CallbackQuery, InlineKeyboardMarkup
from .. import config, db
from ..logger import send_log, card, user_block, chat_block, group_btn
from ..strings import t, sc
from ..utils import member_status

router = Router()
ACTIVE = {"member", "administrator", "creator"}

@router.my_chat_member()
async def on_status(u: ChatMemberUpdated):
    old, new, chat = u.old_chat_member.status, u.new_chat_member.status, u.chat
    if chat.type == "private":
        if new == "kicked": title = "🚫 User blocked the bot"; await db.remove_chat(chat.id)
        elif old == "kicked" and new == "member": title = "✅ User unblocked the bot"
        else: return
        return await send_log(u.bot, card(title, ("👤 User", user_block(u.from_user))))

    if old not in ACTIVE and new in ACTIVE:
        title = "➕ Bot added to group"; await db.get_group(chat.id)
    elif old in ACTIVE and new not in ACTIVE: title = "➖ Bot removed from group"; await db.remove_chat(chat.id)
    elif old == "member" and new == "administrator": title = "⬆️ Bot promoted to admin"
    elif old == "administrator" and new == "member": title = "⬇️ Bot demoted"
    elif old == new == "administrator": title = "🔧 Bot permissions changed"
    else: return

    try: count = await u.bot.get_chat_member_count(chat.id)
    except Exception: count = "?"
    can_del = getattr(u.new_chat_member, "can_delete_messages", None) or new == "creator"
    rows = [("🏘 Group", chat_block(chat)), ("👥 Members", str(count)), ("👤 By", user_block(u.from_user))]
    if new in ACTIVE: rows.append(("🛡 Delete perm", "✅" if can_del else "❌"))
    gb = group_btn(chat)
    await send_log(u.bot, card(title, *rows), InlineKeyboardMarkup(inline_keyboard=[gb]) if gb else None)

    if title.startswith("➕") and not can_del and chat.type != "channel":
        lang = (await db.get_group(chat.id))["lang"]
        try: await u.bot.send_message(chat.id, t(lang, "need_admin"))
        except Exception: pass

@router.callback_query(F.data.startswith("lg:"))
async def log_action(c: CallbackQuery):
    """Log channel me Allow / Ban button — sirf owner ya log chat ke admins."""
    ok = c.from_user.id == config.OWNER_ID or \
         await member_status(c.bot, c.message.chat.id, c.from_user.id) in ("creator", "administrator")
    if not ok: return await c.answer("Not allowed", show_alert=True)
    _, act, chat_id, uid = c.data.split(":"); chat_id, uid = int(chat_id), int(uid)
    if act == "a":
        await db.add_item("allowed", chat_id, uid); res = "✅ Allowed"
    else:
        try: await c.bot.ban_chat_member(chat_id, uid); res = "🚫 Banned"
        except Exception as ex: return await c.answer(f"Ban failed: {ex}"[:190], show_alert=True)
    who = c.from_user.full_name.replace("<", "").replace(">", "")
    await c.message.edit_text(f"{c.message.html_text}\n\n<b>{sc(res)}</b> by {who}", reply_markup=None)
    await c.answer(res)
