import time
import sys
import motor
import pytgcalls as pt
from Music import app, pytgcalls
from pyrogram import filters
from config import OWNER_ID
from Music.core.mongo.usersdb import get_users, add_user, get_user
from Music.core.mongo.chatsdb import get_chats, add_chat, get_chat


# ----------------------------------------------------------- #

start_time = time.time()

@app.on_message(group=10)
async def chat_watcher(_, message):
    try:
        if message.from_user:
            us_in_db = await get_user(message.from_user.id)
            if not us_in_db:
                await add_user(message.from_user.id)

        chat_id = (message.chat.id if message.chat.id != message.from_user.id else None)

        if not chat_id:
            return

        in_db = await get_chat(chat_id)
        if not in_db:
            await add_chat(chat_id)
    except:
        pass

# ----------------------------------------------------------- #

def time_formatter():
    minutes, seconds = divmod(int(time.time() - start_time), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if tmp != "":
        if tmp.endswith(":"):
            return tmp[:-1]
        else:
            return tmp
    else:
        return "0 s"

# ----------------------------------------------------------- #

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    start = time.time()
    users = len(await get_users())
    chats = len(await get_chats())
    activevc = await pytgcalls.calls
    ping = round((time.time() - start) * 1000)
    await message.reply_text(f"""
**Stats of** {(await client.get_me()).mention} :

🏓 **Ping Pong**: `{ping}ms`

📊 **Total Users** : `{users}`
📈 **Totla Chats** : `{chats}`
⚙️ **Bot Uptime** : `{time_formatter()}`
📢 **Active Vc** : `{len(activevc)}`  

🎨 **Python Version** : `{sys.version.split()[0]}`
📑 **Mongo Version** : `{motor.version}`
🥁 **Py-Tgcalls Version** : `{pt.__version__}`
""")
