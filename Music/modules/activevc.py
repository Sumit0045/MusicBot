import os 
from config import OWNER_ID
from pyrogram import filters
from Music import app, pytgcalls




@app.on_message(filters.command("activevc") & filters.user(OWNER_ID))
async def active_voice(_, message):
    msg = await message.reply_text("🔍 Fetching active voice chats...")
    chats = await pytgcalls.calls

    if not chats:
        return await msg.edit_text("❌ No active voice chats found in any group.")

    active_text = f"🎧 Total Active Voice Chats: {len(chats)}\n\n"
    
    for ch in chats:
        try:
            chat = await app.get_chat(ch)
            members = await app.get_chat_members_count(ch)
            title = chat.title or "Unknown"
            username = f"@{chat.username}" if chat.username else "No Username"
            active_text += f"🔹 {title}\n    ↳ {username} | 👥 Members: {members}\n\n"
        except Exception:
            active_text += f"⚠️ Failed to fetch info for {ch}\n"

    if len(chats) > 10 or len(active_text) > 4000:
        file_path = "active_voice_chats.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(active_text)

        await message.reply_document(file_path, caption="🎧 **Active Voice Chats List**")
        await msg.delete()
        os.remove(file_path)
    else:
        await msg.edit_text(active_text)


