"""Auto promo: roz PROMO_AT (default 07:00 IST) pe live post sabko. /autopromo se control."""
import asyncio, logging
from datetime import datetime
from zoneinfo import ZoneInfo
from . import checks, config, db
from .broadcast import blast, live_sender
from .logger import card, send_log

log = logging.getLogger("roohiremov")

async def promo_loop(bot):
    me = await bot.get_me()
    hh, mm = (int(x) for x in config.PROMO_AT.split(":"))
    while True:
        try:
            await asyncio.sleep(30)
            c = await db.cfg_all(0)                                   # chat_id 0 = global bot settings
            if c.get("promo_on", "1" if config.AUTO_PROMO else "0") != "1": continue
            now = datetime.now(ZoneInfo(config.PROMO_TZ))
            if not checks.is_due(now, hh, mm, c.get("promo_last", "")): continue
            await db.cfg_set(0, "promo_last", now.strftime("%Y-%m-%d"))
            await send_log(bot, card("📣 Auto promo started", ("🕒 Schedule", f"{config.PROMO_AT} {config.PROMO_TZ}")))
            res = await blast(bot, "all", live_sender(bot, me.username))
            if res is None:                                           # manual broadcast chal raha tha -> 30s baad retry
                await db.cfg_set(0, "promo_last", ""); continue
            await send_log(bot, card("📣 Auto promo finished", ("✅ Sent", str(res["ok"])),
                                     ("🗑 Removed (dead)", str(res["gone"])), ("❌ Failed", str(res["fail"]))))
            if c.get("promo_mode", "daily") == "once":
                await db.cfg_set(0, "promo_on", "0")
        except asyncio.CancelledError:
            raise
        except Exception:
            log.exception("promo loop error")
