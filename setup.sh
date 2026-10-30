#!/usr/bin/env bash
# RoohiRemov — one-command VPS setup (Ubuntu/Debian)
# Use:  bash setup.sh        (pehli baar: install + .env + service)
#       bash setup.sh update (git pull + restart)
set -e

REPO="https://github.com/konbkl/RoohiRemov.git"
SERVICE="roohiremov"
SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"

# repo ke andar se chalaya to wahi use karo, warna ~/RoohiRemov me clone
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$HERE/main.py" ]; then DIR="$HERE"; else DIR="$HOME/RoohiRemov"; fi

if [ "$1" = "update" ]; then
  cd "$DIR"; git pull
  ./venv/bin/pip install -q -U -r requirements.txt
  $SUDO systemctl restart $SERVICE
  echo "✅ Updated & restarted"; exit 0
fi

echo "📦 Installing packages..."
$SUDO apt-get update -y
$SUDO apt-get install -y git python3 python3-venv python3-pip

if [ ! -f "$DIR/main.py" ]; then
  echo "⬇️  Cloning repo..."; git clone "$REPO" "$DIR"
fi
cd "$DIR"

echo "🐍 Setting up virtualenv..."
[ -d venv ] || python3 -m venv venv
./venv/bin/pip install -q -U pip
./venv/bin/pip install -q -U -r requirements.txt

if [ ! -f .env ]; then
  echo; echo "📝 .env bharte hain (Enter dabaoge to khali/default rahega)"
  while [ -z "$BOT_TOKEN" ]; do read -rp "BOT_TOKEN (@BotFather): " BOT_TOKEN; done
  read -rp "OWNER_ID (@userinfobot se): " OWNER_ID
  read -rp "LOG_CHAT_ID (-100...): " LOG_CHAT_ID
  read -rp "UPDATES_URL: " UPDATES_URL
  read -rp "SUPPORT_URL: " SUPPORT_URL
  read -rp "START_IMG (photo URL/file_id): " START_IMG
  read -rp "MONGO_URI (khali = SQLite): " MONGO_URI
  cat > .env <<ENV
BOT_TOKEN=$BOT_TOKEN
OWNER_ID=$OWNER_ID
LOG_CHAT_ID=$LOG_CHAT_ID
UPDATES_URL=${UPDATES_URL:-https://t.me/telegram}
SUPPORT_URL=${SUPPORT_URL:-https://t.me/telegram}
START_IMG=$START_IMG
MONGO_URI=$MONGO_URI
MONGO_DB=roohiremov
DB_PATH=roohiremov.db
PREMIUM_EMOJI=false
ENV
  chmod 600 .env
  echo "✅ .env bana diya"
else
  echo "ℹ️  .env pehle se hai, chhoda nahi"
fi

echo "⚙️  Creating service..."
$SUDO tee /etc/systemd/system/$SERVICE.service > /dev/null <<UNIT
[Unit]
Description=RoohiRemov Bot
After=network.target

[Service]
User=$(id -un)
WorkingDirectory=$DIR
ExecStart=$DIR/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT

$SUDO systemctl daemon-reload
$SUDO systemctl enable --now $SERVICE
sleep 3
$SUDO systemctl --no-pager status $SERVICE | head -n 12 || true

cat <<MSG

🚀 Done! Useful commands:
  journalctl -u $SERVICE -f          # live logs
  sudo systemctl restart $SERVICE    # restart
  bash setup.sh update               # update from GitHub
MSG
