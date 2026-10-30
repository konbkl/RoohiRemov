# RoohiRemov 🔗✂️
Telegram group link-remover bot (aiogram 3 + SQLite).

## Features
- Users / bots / channels ke links auto-delete, caption links bhi
- Invite links, t.me links, @usernames filter
- `/allow` `/disallow` `/allowed` — approved users
- `/whitelist` `/rwhitelist` — max 10 allowed links
- `/blacklist` `/rblacklist` `/blacklisted` — word/phrase filter
- `/settings` toggle panel, `/language` (9 languages, translations `strings.py` me add karo)
- Owner admins ka edit access band/chalu kar sakta hai

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env   # BOT_TOKEN, OWNER_ID bharo
python main.py
```
Bot ko group me add karo + **Delete Messages** permission do.

## UI / Font / Languages
- Default language English; 10 languages (English, Hinglish, Hindi, Burmese, Uzbek, Russian, Arabic, Spanish, French, Bengali), sabhi keys translated (`strings.py`).
- Font mapping `strings.py` ke `_MAP` me hai (Λ ε σ η style) — chaho to edit karo.
- Welcome = greeting quote + expandable blockquote; buttons coloured (blue/red/green) — Telegram ka naya button `style` field.
- `SUPPORT_URL` aur `UPDATES_URL` `.env` me.

## Database
`MONGO_URI` bharo to MongoDB (broadcast/stats bhi isi se), khali to SQLite file (`DB_PATH`). Dono me same features.

## Logger
`.env` me `LOG_CHAT_ID` daalo (channel/group, bot wahan admin ho). In events ka log aayega:
bot start/stop, bot kisi group me add/remove/admin, user ka /start, user ne bot block/unblock kiya,
har deleted message (link/blacklist), aur errors. Sirf wahi messages log hote hain jo bot delete kare (har message log nahi hota). Card pe Allow / Ban quick buttons. File log: `logs/roohiremov.log`.

## Owner commands (private me)
`/stats`, `/broadcast <text>` (ya reply), `/live` (launch message sab ko)

## Banner photo
Bot ko logo photo bhejo, uska file_id ya URL `.env` ke `START_IMG` me daalo.

## Premium emoji
1. `RoohiRemov/emojis.py` me har `ID_HERE` ki jagah custom emoji ID daalo (@GetEmojiIDbot ko premium emoji forward karo).
2. `.env` me `PREMIUM_EMOJI=true`.
Note: Telegram ke rule ke hisaab se bots ke messages me custom emoji tabhi dikhte hain jab bot ne Fragment pe extra username kharida ho. Warna normal emoji fallback dikhega.

## Structure
```
main.py
RoohiRemov/
  config.py db.py emojis.py strings.py utils.py
  modules/ start settings language users whitelist blacklist remover
```


## Heroku (worker dyno, Basic)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/konbkl/RoohiRemov)

Heroku ki disk ephemeral hoti hai, isliye **MONGO_URI zaroori hai** (SQLite restart pe reset ho jata hai).
```bash
heroku create roohiremov --stack heroku-24
heroku config:set BOT_TOKEN=... OWNER_ID=... MONGO_URI=... LOG_CHAT_ID=-100...
git push heroku main
heroku ps:scale web=0 worker=1
heroku logs -t
```

## Owner commands (private)
`/broadcast text` (sab), `/broadcast -user text`, `/broadcast -group text`, reply + `/broadcast` (media copy),
`/live` (launch post, `-user` / `-group` bhi), `/stats`. `/ping` sab ke liye.

## Auto promo (daily 7 AM)
Roz `PROMO_AT` (default 07:00, `PROMO_TZ=Asia/Kolkata`) pe launch post (image `assets/promo.png` ke saath) sab users, groups aur channels ko jata hai.
Owner commands: `/autopromo daily` (roz), `/autopromo once` (sirf ek baar), `/autopromo off`. Bot 3 ghante se zyada late ho to us din skip karta hai.
