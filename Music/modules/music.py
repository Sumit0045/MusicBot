import os, random, asyncio
from pyrogram import filters, enums
from Music import app, pytgcalls, userbot
from pyrogram.errors import UserAlreadyParticipant
from Music.core import core_func, main_func, thumb_func
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality
from pytgcalls import filters as call_filters
from youtube_search import YoutubeSearch


is_active = {}
is_paused = {}

local_thumb = [
"https://graph.org/file/e3fa9ab16ebefbfdd29d9.jpg",
"https://graph.org/file/5938774f48c1f019c73f7.jpg",
"https://graph.org/file/b13a16734bab174f58482.jpg",
"https://graph.org/file/2deb4e5cbba862f2d5457.jpg",
]

def parse_duration(duration_str):
    try:
        parts = duration_str.split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except:
        return 0
    return 0



# -------------------------- Play-Commands -------------------------- #

@app.on_message(filters.command(["play", "vplay"], prefixes=["/", "."]))
async def play_music(_, message):
    chat_id = message.chat.id
    user_name = message.from_user.mention
    
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("<i>Hello handsome, this command only works in groups, not in private.</i>")
                  
    msg = await message.reply("🔍 **Searching...**")
    
    try:
        user = await userbot.get_me()
        await _.get_chat_member(chat_id, user.id)
    except:      
        try:
            invitelink = await _.export_chat_invite_link(chat_id)
        except Exception:    
            await msg.edit_text("**» ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғɪʀsᴛ.**")
        try:
            await userbot.join_chat(invitelink)
            await message.reply_text("** ✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
        except UserAlreadyParticipant:            
            pass
        except Exception as e:
            await msg.edit_text(f"**ᴘʟᴇᴀsᴇ ᴍᴀɴᴜᴀʟʟʏ ᴀᴅᴅ ᴀssɪsᴛᴀɴᴛ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ [sᴜᴍɪᴛ ʏᴀᴅᴀᴠ](https://t.me/AnonDeveloper)**")

    
    media = message.reply_to_message
    file_path = None
    music_thumb = None
    video = False

    if media:
        duration_sec = round(
            (media.audio.duration if media.audio else
             media.video.duration if media.video else
             media.voice.duration if media.voice else 0)
        )
        duration_min = round(duration_sec / 60)
        title = (
            getattr(media.audio, "title", None) or
            getattr(media.audio, "file_name", None) or
            getattr(media.video, "file_name", None) or
            ("Voice Message" if media.voice else "Unknown Title")
        )
        thumbnail = random.choice(local_thumb)
        views = "Locally Added"
        channel = "Music Player"

        if duration_min > 300:
            return await msg.edit_text("🛑 Song longer than 300 minutes are not allowed.")

        file_path = await asyncio.create_task(media.download())
        music_thumb = await thumb_func.generate_cover(title, views, duration_min, thumbnail, channel)

    else:
        if len(message.command) < 2:
            return await msg.edit_text("💌 **Usage:** `/play or /vplay <song name>`")

        command = message.command[0].lower()
        video = command == "vplay"
        if video:
            return await msg.edit_text("bruh already i told you adding vplay in next update.")
        await msg.edit("▓▓▓▓▓▓▓▓▓▓▓ 100%\n\n**⇆ ᴘʀᴏᴄᴇssɪɴɢ...**")

        query = message.text.split(None, 1)[1]

        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            if not results:
                return await msg.edit_text("🛑 Song Not Found!!")

            result = results[0]
            title = result["title"]
            duration_str = result["duration"]
            duration_sec = parse_duration(duration_str)
            duration_min = round(duration_sec / 60)
            views = result["views"]
            thumbnail = result["thumbnails"][1]
            channel = result["channel"]
            url = f"https://youtu.be/{result['id']}"

            if duration_min > 300:
                return await msg.edit_text("🛑 Song longer than 300 minutes are not allowed.")

            await msg.edit("🎶 Generating download URL...")
            download_url = await main_func.youtube_api(url)
            print(download_url)
            file_path = await asyncio.create_task(main_func.get_audio_stream(download_url, title))
            music_thumb = await thumb_func.generate_cover(title, views, duration_min, thumbnail, channel)

        except Exception as e:
            return await msg.edit_text(f"Error: {e}")

    if not file_path:
        return await msg.edit_text("⚠️ Failed To Download Media.")

    if is_active.get(chat_id):
        position = await core_func.put(
            chat_id,
            file=file_path,
            thumbnail=music_thumb,
            video=video,
            title=title,
            duration=duration_min,
            user=user_name
        )
        await message.reply_photo(
            photo=music_thumb,
            caption=(
                f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position} **\n\n"
                f"🏷️ **ɴᴀᴍᴇ :** {title[:30]}\n"
                f"⏰ **ᴅᴜʀᴀᴛɪᴏɴ :** `{duration_min}` **ᴍɪɴᴜᴛᴇs**\n"
                f"👀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ: **{user_name}"
            )
        )
    else:
        await pytgcalls.play(
            chat_id=chat_id,
            stream=MediaStream(
                audio_path=file_path,
                media_path=file_path,
                audio_parameters=AudioQuality.HIGH if not video else AudioQuality.STUDIO,
                video_parameters=VideoQuality.FHD_1080p if video else VideoQuality.SD_360p,
                audio_flags=MediaStream.Flags.REQUIRED,
                video_flags=MediaStream.Flags.AUTO_DETECT if video else MediaStream.Flags.IGNORE,
            )
        )
        await message.reply_photo(
            photo=music_thumb,
            caption=(
                f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n\n"
                f"🏷️ **ɴᴀᴍᴇ :** {title[:30]}\n"
                f"⏰ **ᴅᴜʀᴀᴛɪᴏɴ :** `{duration_min}` ᴍɪɴᴜᴛᴇs\n"
                f"👀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{user_name}"
            )
        )
        is_active[chat_id] = True
    await msg.delete()
    




# -------------------------- Multi-Commands -------------------------- #

@app.on_message(filters.command(["skip", "next", "leave", "left", "end", "volume", "pause", "resume", "loop", "join"], prefixes=["/", "!"]))
async def multi_commands(_, message):
    chat_id = message.chat.id
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("<i>Hello handsome, this command only works in groups, not in private.</i>")
              
    check = await main_func.is_admin(_, message)
    if check == False:
        return 
        
    command = message.command[0].lower()

    if command in ["skip", "next"]:
        if chat_id not in is_active or not is_active[chat_id]:
            return await message.reply_text("**🎧 ɴᴏᴛʜɪɴɢ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ ᴛᴏ sᴋɪᴘ.**")

        core_func.task_done(chat_id)

        if core_func.is_empty(chat_id):
            await pytgcalls.leave_call(chat_id)
            is_active[chat_id] = False
            await message.reply_text("**🛑 ᴘʟᴀʏʟɪsᴛ ғɪɴɪsʜᴇᴅ. ʟᴇғᴛ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.**")
        else:
            next_song = core_func.get(chat_id)
            file_path = next_song["file"]
            thumbnail = next_song["thumbnail"]
            video = next_song["video"]
            title = next_song["title"]
            duration = next_song["duration"]
            requested_by = next_song["user"]   
            
            await pytgcalls.play(
                chat_id=chat_id,
                stream=MediaStream(
                    audio_path=file_path,
                    media_path=file_path,
                    audio_parameters=AudioQuality.HIGH if video else AudioQuality.STUDIO,
                    video_parameters=VideoQuality.FHD_1080p if video else VideoQuality.SD_360p,
                    audio_flags=MediaStream.Flags.REQUIRED,
                    video_flags=MediaStream.Flags.AUTO_DETECT if video else MediaStream.Flags.IGNORE,
                )
            )
            await message.reply_photo(
                photo=thumbnail,
                caption=(
                  f"**➻ sᴋɪᴘᴘᴇᴅ ᴛᴏ ɴᴇxᴛ sᴏɴɢ**\n\n"
                  f"🏷️ **ɴᴀᴍᴇ :** {title[:30]}\n"
                  f"⏰ **ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n"
                  f"👀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{requested_by}"
                )
            )

    elif command in ["leave", "left", "end"]:
        if chat_id not in is_active or not is_active[chat_id]:
            return await message.reply_text("**🎧 ɴᴏ ᴍᴜsɪᴄ ɪs ᴘʟᴀʏɪɴɢ ᴄᴜʀʀᴇɴᴛʟʏ.**")
        await pytgcalls.leave_call(chat_id)
        is_active[chat_id] = False
        await message.reply_text("**👋 ʟᴇғᴛ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.**")

    elif command == "volume":
        args = message.text.split()
        if len(args) == 2 and args[1].isdigit():
            if chat_id not in is_active or not is_active[chat_id]:
                return await message.reply_text("**🎧 ᴄᴀɴ'ᴛ ᴀᴅᴊᴜsᴛ ᴠᴏʟᴜᴍᴇ — ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.**")
            
            volume = int(args[1])
            if volume > 200:
                await message.reply_text("**🔒 ᴠᴏʟᴜᴍᴇ ᴍᴜsᴛ ʙᴇ ʙᴇᴛᴡᴇᴇɴ 1% ᴀɴᴅ 200%.**")
            else:
                await pytgcalls.change_volume_call(chat_id, volume)
                await message.reply_text(f"**🔊 ᴠᴏʟᴜᴍᴇ sᴇᴛ ᴛᴏ {volume}%**")
        else:
            await message.reply_text("**📝 ᴜsᴀɢᴇ:** `/volume 1-200`")

    elif command == "pause":
        if chat_id not in is_active or not is_active[chat_id]:
            return await message.reply_text("**🎧 ɴᴏ ᴍᴜsɪᴄ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ.**")
        
        if is_paused.get(chat_id, {}).get("paused"):
            return await message.reply_text("**⏸️ ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜsᴇᴅ.**")
        
        await pytgcalls.pause(chat_id)
        is_paused[chat_id] = {"paused": True}
        await message.reply_text("**⏸️ ᴘʟᴀʏʙᴀᴄᴋ ᴘᴀᴜsᴇᴅ.**")

    elif command == "resume":
        if chat_id not in is_active or not is_active[chat_id]:
            return await message.reply_text("**🎧 ɴᴏ ᴍᴜsɪᴄ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ.**")

        if not is_paused.get(chat_id, {}).get("paused"):
            return await message.reply_text("**▶️ ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴘʟᴀʏɪɴɢ.**")
        
        await pytgcalls.resume(chat_id)
        is_paused[chat_id]["paused"] = False
        await message.reply_text("**▶️ ʀᴇsᴜᴍᴇᴅ ᴘʟᴀʏʙᴀᴄᴋ.**")

    elif command == "loop":
        await message.reply_text("**🔁 ʟᴏᴏᴘ ғᴇᴀᴛᴜʀᴇ ɪs ɴᴏᴛ ɪᴍᴘʟᴇᴍᴇɴᴛᴇᴅ ʏᴇᴛ. sᴛᴀʏ ᴛᴜɴᴇᴅ!**")

    elif command == "join":
        try:
            user = await userbot.get_me()
            await _.get_chat_member(chat_id, user.id)
        except:      
            try:
                invitelink = await _.export_chat_invite_link(chat_id)
            except Exception:    
                await msg.edit_text("**» ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғɪʀsᴛ.**")
            try:
                await userbot.join_chat(invitelink)
                await message.reply_text("** ✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
            except UserAlreadyParticipant:            
                pass
            except Exception as e:
                await message.reply_text(f"**ᴘʟᴇᴀsᴇ ᴍᴀɴᴜᴀʟʟʏ ᴀᴅᴅ ᴀssɪsᴛᴀɴᴛ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ [sᴜᴍɪᴛ ʏᴀᴅᴀᴠ](https://t.me/AnonDeveloper)**\n\nᴀssɪsᴛᴀɴᴛ - @{user.username}")



# -------------------------- Auto-Stream-Update -------------------------- #

@pytgcalls.on_update(call_filters.stream_end())
async def on_stream_end(_, update):
    chat_id = update.chat_id    
    core_func.task_done(chat_id)

    if core_func.is_empty(chat_id):
        await pytgcalls.leave_call(chat_id)
        is_active[chat_id] = False
        await app.send_message(chat_id, "😜 No More Songs!! Leaving VC.")
            
    else:
        next_song = core_func.get(chat_id)
        file_path = next_song["file"]
        thumbnail = next_song["thumbnail"]
        video = next_song["video"]
        title = next_song["title"]
        duration = next_song["duration"]
        requested_by = next_song["user"]

        await pytgcalls.play(
            chat_id=chat_id,
            stream=MediaStream(
                audio_path=file_path,
                media_path=file_path,
                audio_parameters=AudioQuality.HIGH if video else AudioQuality.STUDIO,
                video_parameters=VideoQuality.FHD_1080p if video else VideoQuality.SD_360p,
                audio_flags=MediaStream.Flags.REQUIRED,
                video_flags=MediaStream.Flags.AUTO_DETECT if video else MediaStream.Flags.IGNORE,
            )
        )

        await app.send_photo(
            chat_id=chat_id,
            photo=thumbnail,
            caption=(
                f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n\n"
                f"🏷️ **ɴᴀᴍᴇ :** {title[:30]}\n"
                f"⏰ **ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n"
                f"👀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{requested_by}"
            )
        )
            

