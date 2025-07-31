from Music import app
from pyrogram import filters
from Music.core import script
from Music.modules.start import private_buttons as buttons
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@app.on_callback_query()
async def handle_callback(_, query):
    user_id = query.from_user.id
    try:
        clicked = query.message.reply_to_message.from_user.id
    except:
        clicked = query.from_user.id

    try:
        if user_id != clicked:
            return await query.answer("This button isn’t for you!", show_alert=True)

        if query.data == "guide_":
            back_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="start_")]
            ])
            await query.message.edit_text(script.GUIDE_TEXT, reply_markup=back_button)

        elif query.data == "start_":
            await query.message.edit_text(script.START_TEXT.format(query.from_user.mention), reply_markup=buttons)

        elif query.data == "maintainer_":
            await query.answer(
                "🚧 Feature Coming Soon!\nBot is under maintenance. Please stay tuned.",
                show_alert=True
            )

        elif query.data == "close_data":
            try:
                await query.message.delete()
                if query.message.reply_to_message:
                    await query.message.reply_to_message.delete()
            except Exception as e:
                print(f"**Error deleting message**: {e}")

    except Exception as e:
        print(f"**Error**: {e}")
        await query.message.reply_text(f"**Error**\n```{e}```")
