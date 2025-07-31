import config
from Music import app, BOT_USERNAME
from pyrogram import filters, enums
from Music.core import script
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


# -------------------------- Buttons -------------------------- #

private_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🔎 Support", url=config.SUPPORT_CHANNEL),
        InlineKeyboardButton("📢 Updates", url=config.UPDATES_CHANNEL)
    ],
    [
        InlineKeyboardButton("🌱 Quick Guide", callback_data="guide_")
    ]
])

group_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Click Me", url=f"https://t.me/{BOT_USERNAME}?start=true")
    ],
    [
        InlineKeyboardButton("Add to Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
    ]
])


# -------------------------- Start -------------------------- #

@app.on_message(filters.command("start"))
async def start_(_, message):
    name = message.from_user.mention

    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_photo(photo="https://graph.org/file/ffbaa6d0fe89bdf98886b-9760febe78f97be25e.jpg",                         
            caption=script.START_TEXT.format(name),
            reply_markup=private_buttons
        )
    else:
        await message.reply_photo(photo="https://graph.org/file/ffbaa6d0fe89bdf98886b-9760febe78f97be25e.jpg",
            caption=f"Hello {name}! 💕 If you need any help, don’t hesitate to message me!",
            reply_markup=group_buttons
        )

            
