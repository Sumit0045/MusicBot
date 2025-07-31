import os, yt_dlp
import requests, asyncio
from pyrogram.enums import ChatMemberStatus


async def is_admin(app, message):
  check_status = await app.get_chat_member(message.chat.id, message.from_user.id)
  if check_status.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
    await message.reply_text("<i>You are not an administrator or owner, so you cannot use this command.</i>")
    return False
  else:
    return True
      

async def check_progress(session, url):
    response = session.get(url)
    if response.ok:
        data = response.json()
        if data.get("text") == "Finished" and int(data.get("progress", 0)) == 1000:
            return data.get("download_url")
    await asyncio.sleep(3)
    return await check_progress(session, url)


async def youtube_api(url):
    session = requests.Session()
    api_url = "https://p.oceansaver.in/ajax/download.php"
    params = {
        "copyright": "0",
        "format": "mp3",
        "url": url,
        "api": "dfcb6d76f2f6a9894gjkege8a4ab232222"
    }
    response = session.get(api_url, params=params)

    if response.ok:
        data = response.json()
        progress_url = data.get("progress_url")
        if progress_url:
            download_url = await check_progress(session, progress_url)
            return download_url
    return None




async def get_audio_stream(link, filename=None):
    os.makedirs("downloads", exist_ok=True)
    
    ydl_opts = {
        "format": "bestaudio/best",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
        "outtmpl": f"downloads/{filename}.%(ext)s" if filename else "downloads/%(id)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        if filename:
            ext = info.get("ext", "webm")
            path = f"downloads/{filename}.{ext}"
        else:
            path = ydl.prepare_filename(info)
        return path





