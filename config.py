from os import getenv

API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = list(map(int, getenv("OWNER_ID", "").split()))
MONGO_DB = getenv("MONGO_DB", "")
SESSION_STRING = getenv("SESSION_STRING", "")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "https://t.me/DevsLaboratory")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/DevsHubChat")
