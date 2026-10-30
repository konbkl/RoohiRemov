import asyncio, html, logging, os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import ErrorEvent
from RoohiRemov import config, db
from RoohiRemov.scheduler import promo_loop
from RoohiRemov.logger import setup_logging, send_log, log_startup, log_shutdown, card
from RoohiRemov.modules import start, settings, language, users, whitelist, blacklist, automod, ping, owner, logs, remover

async def main():
    setup_logging()
    await db.init()
    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    # remover SABSE LAST rahna chahiye (catch-all)
    dp.include_routers(*(m.router for m in (start, settings, language, users, whitelist, blacklist, automod, ping, owner, logs, remover)))

    @dp.errors()
    async def on_error(event: ErrorEvent):
        logging.error("Update error", exc_info=event.exception)
        await send_log(bot, f"🔥 <b>ERROR</b>\n<code>{html.escape(repr(event.exception))[:3000]}</code>")
        return True

    await bot.delete_webhook(drop_pending_updates=True)
    await log_startup(bot)
    if os.getenv("DYNO") and not db.USE_MONGO:
        await send_log(bot, card("⚠️ Heroku + SQLite", ("Note", "Heroku disk is ephemeral: data resets on every restart. Set MONGO_URI.")))
    promo_task = asyncio.create_task(promo_loop(bot))
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        promo_task.cancel()
        await log_shutdown(bot)
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
