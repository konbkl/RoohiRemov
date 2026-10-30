"""Database: MONGO_URI set ho to MongoDB, warna SQLite. Dono ka interface same hai."""
import time
import aiosqlite
from . import config

COLS = {"lang","block_users","block_bots","block_channels","block_captions","block_usernames","admins_can_edit"}
TABLES = {"allowed","whitelist","blacklist","abuse"}
DEFAULTS = dict(lang="en", block_users=1, block_bots=1, block_channels=1,
                block_captions=1, block_usernames=1, admins_can_edit=1)
USE_MONGO = bool(config.MONGO_URI)

# ======================= SQLite =======================
SCHEMA = """
CREATE TABLE IF NOT EXISTS groups(
 chat_id INTEGER PRIMARY KEY, lang TEXT DEFAULT 'en',
 block_users INTEGER DEFAULT 1, block_bots INTEGER DEFAULT 1,
 block_channels INTEGER DEFAULT 1, block_captions INTEGER DEFAULT 1,
 block_usernames INTEGER DEFAULT 1, admins_can_edit INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS allowed(chat_id INTEGER, val TEXT, PRIMARY KEY(chat_id,val));
CREATE TABLE IF NOT EXISTS whitelist(chat_id INTEGER, val TEXT, PRIMARY KEY(chat_id,val));
CREATE TABLE IF NOT EXISTS blacklist(chat_id INTEGER, val TEXT, PRIMARY KEY(chat_id,val));
CREATE TABLE IF NOT EXISTS stats(key TEXT PRIMARY KEY, val INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS abuse(chat_id INTEGER, val TEXT, PRIMARY KEY(chat_id,val));
CREATE TABLE IF NOT EXISTS cfg(chat_id INTEGER, key TEXT, val TEXT, PRIMARY KEY(chat_id,key));
"""

async def _sq_init():
    async with aiosqlite.connect(config.DB_PATH) as d:
        await d.executescript(SCHEMA); await d.commit()

async def _sq_get_group(chat_id):
    async with aiosqlite.connect(config.DB_PATH) as d:
        d.row_factory = aiosqlite.Row
        await d.execute("INSERT OR IGNORE INTO groups(chat_id) VALUES(?)", (chat_id,))
        await d.commit()
        cur = await d.execute("SELECT * FROM groups WHERE chat_id=?", (chat_id,))
        return dict(await cur.fetchone())

async def _sq_set_group(chat_id, **kw):
    await _sq_get_group(chat_id)
    sets = ",".join(f"{k}=?" for k in kw)
    async with aiosqlite.connect(config.DB_PATH) as d:
        await d.execute(f"UPDATE groups SET {sets} WHERE chat_id=?", (*kw.values(), chat_id))
        await d.commit()

async def _sq_add(table, chat_id, val):
    async with aiosqlite.connect(config.DB_PATH) as d:
        cur = await d.execute(f"INSERT OR IGNORE INTO {table} VALUES(?,?)", (chat_id, str(val)))
        await d.commit(); return cur.rowcount > 0

async def _sq_del(table, chat_id, val):
    async with aiosqlite.connect(config.DB_PATH) as d:
        cur = await d.execute(f"DELETE FROM {table} WHERE chat_id=? AND val=?", (chat_id, str(val)))
        await d.commit(); return cur.rowcount > 0

async def _sq_list(table, chat_id):
    async with aiosqlite.connect(config.DB_PATH) as d:
        cur = await d.execute(f"SELECT val FROM {table} WHERE chat_id=?", (chat_id,))
        return [r[0] for r in await cur.fetchall()]

async def _sq_chats():
    async with aiosqlite.connect(config.DB_PATH) as d:
        cur = await d.execute("SELECT chat_id, lang FROM groups")
        return [tuple(r) for r in await cur.fetchall()]

async def _sq_incr(key):
    async with aiosqlite.connect(config.DB_PATH) as d:
        await d.execute("INSERT INTO stats(key,val) VALUES(?,1) ON CONFLICT(key) DO UPDATE SET val=val+1", (key,))
        await d.commit()

async def _sq_stat(key):
    async with aiosqlite.connect(config.DB_PATH) as d:
        cur = await d.execute("SELECT val FROM stats WHERE key=?", (key,))
        r = await cur.fetchone(); return r[0] if r else 0

async def _sq_remove_chat(chat_id):
    async with aiosqlite.connect(config.DB_PATH) as d:
        for tb in ("groups", "allowed", "whitelist", "blacklist", "abuse", "cfg"):
            await d.execute(f"DELETE FROM {tb} WHERE chat_id=?", (chat_id,))
        await d.commit()

async def _sq_cfg_all(chat_id):
    async with aiosqlite.connect(config.DB_PATH) as d:
        cur = await d.execute("SELECT key,val FROM cfg WHERE chat_id=?", (chat_id,))
        return {k: v for k, v in await cur.fetchall()}

async def _sq_cfg_set(chat_id, key, val):
    async with aiosqlite.connect(config.DB_PATH) as d:
        await d.execute("INSERT INTO cfg(chat_id,key,val) VALUES(?,?,?) ON CONFLICT(chat_id,key) DO UPDATE SET val=excluded.val",
                        (chat_id, key, str(val)))
        await d.commit()

# ======================= MongoDB =======================
if USE_MONGO:
    from motor.motor_asyncio import AsyncIOMotorClient
    from pymongo import ReturnDocument
    from pymongo.errors import DuplicateKeyError
    _mdb = AsyncIOMotorClient(config.MONGO_URI)[config.MONGO_DB]

async def _mg_init():
    await _mdb.items.create_index([("chat_id", 1), ("table", 1), ("val", 1)], unique=True)

async def _mg_get_group(chat_id):
    doc = await _mdb.groups.find_one_and_update(
        {"_id": chat_id}, {"$setOnInsert": DEFAULTS}, upsert=True, return_document=ReturnDocument.AFTER)
    doc["chat_id"] = doc.pop("_id")
    return doc

async def _mg_set_group(chat_id, **kw):
    await _mg_get_group(chat_id)
    await _mdb.groups.update_one({"_id": chat_id}, {"$set": kw})

async def _mg_add(table, chat_id, val):
    try:
        await _mdb.items.insert_one({"chat_id": chat_id, "table": table, "val": str(val)}); return True
    except DuplicateKeyError:
        return False

async def _mg_del(table, chat_id, val):
    r = await _mdb.items.delete_one({"chat_id": chat_id, "table": table, "val": str(val)})
    return r.deleted_count > 0

async def _mg_list(table, chat_id):
    return [d["val"] async for d in _mdb.items.find({"chat_id": chat_id, "table": table})]

async def _mg_chats():
    return [(d["_id"], d.get("lang", "en")) async for d in _mdb.groups.find({}, {"lang": 1})]

async def _mg_incr(key):
    await _mdb.stats.update_one({"_id": key}, {"$inc": {"val": 1}}, upsert=True)

async def _mg_stat(key):
    d = await _mdb.stats.find_one({"_id": key}); return d["val"] if d else 0

async def _mg_remove_chat(chat_id):
    await _mdb.groups.delete_one({"_id": chat_id})
    await _mdb.items.delete_many({"chat_id": chat_id})
    await _mdb.cfg.delete_many({"chat_id": chat_id})

async def _mg_cfg_all(chat_id):
    return {d["key"]: d["val"] async for d in _mdb.cfg.find({"chat_id": chat_id})}

async def _mg_cfg_set(chat_id, key, val):
    await _mdb.cfg.update_one({"_id": f"{chat_id}:{key}"}, {"$set": {"chat_id": chat_id, "key": key, "val": str(val)}}, upsert=True)

# ======================= Public API =======================
async def init():
    await (_mg_init() if USE_MONGO else _sq_init())

async def get_group(chat_id: int) -> dict:
    return await (_mg_get_group(chat_id) if USE_MONGO else _sq_get_group(chat_id))

async def set_group(chat_id: int, **kw):
    assert set(kw) <= COLS
    await (_mg_set_group(chat_id, **kw) if USE_MONGO else _sq_set_group(chat_id, **kw))

async def add_item(table, chat_id, val) -> bool:
    assert table in TABLES
    return await (_mg_add if USE_MONGO else _sq_add)(table, chat_id, val)

async def del_item(table, chat_id, val) -> bool:
    assert table in TABLES
    return await (_mg_del if USE_MONGO else _sq_del)(table, chat_id, val)

async def list_items(table, chat_id) -> list[str]:
    assert table in TABLES
    return await (_mg_list if USE_MONGO else _sq_list)(table, chat_id)

async def count_items(table, chat_id) -> int:
    return len(await list_items(table, chat_id))

async def chats() -> list[tuple[int, str]]:
    """(chat_id, lang) — chat_id>0 = private users, <0 = groups. Broadcast/stats isi se."""
    return await (_mg_chats() if USE_MONGO else _sq_chats())

async def incr_stat(key: str):
    await (_mg_incr(key) if USE_MONGO else _sq_incr(key))

async def get_stat(key: str) -> int:
    return await (_mg_stat(key) if USE_MONGO else _sq_stat(key))

async def remove_chat(chat_id: int):
    _cfg_cache.pop(chat_id, None)
    """Bot group se nikla / user ne block kiya -> data hata do (stats sahi rahe)."""
    await (_mg_remove_chat(chat_id) if USE_MONGO else _sq_remove_chat(chat_id))

_cfg_cache: dict[int, tuple[float, dict]] = {}

async def cfg_all(chat_id: int) -> dict:
    """Module settings (phone/promo/fsub/...) — 30s cache."""
    hit = _cfg_cache.get(chat_id)
    if hit and time.time() - hit[0] < 30: return hit[1]
    data = await (_mg_cfg_all if USE_MONGO else _sq_cfg_all)(chat_id)
    _cfg_cache[chat_id] = (time.time(), data); return data

async def cfg_set(chat_id: int, key: str, val):
    await (_mg_cfg_set if USE_MONGO else _sq_cfg_set)(chat_id, key, val)
    _cfg_cache.pop(chat_id, None)
