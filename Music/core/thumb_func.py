import os
import random
import aiofiles
import aiohttp
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import ffmpeg


def make_col():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


def convert_seconds(seconds):
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


def time_to_seconds(time):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(time).split(":"))))


def truncate(text):
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < 27:
            text1 += " " + word
        elif len(text2) + len(word) < 25:
            text2 += " " + word
    return [text1.strip(), text2.strip()]


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(title, views, duration, thumbnail_url, channel):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail_url) as resp:
            if resp.status == 200:
                async with aiofiles.open("background.png", mode="wb") as f:
                    await f.write(await resp.read())

    bg_image = Image.open("background.png")
    black_overlay = Image.open(r"Music/core/resources/black.jpg")
    music_overlay = Image.open(r"Music/core/resources/music.png")
    music_overlay = changeImageSize(1280, 720, music_overlay)

    blurred_bg = changeImageSize(1280, 720, bg_image).filter(ImageFilter.BoxBlur(20))
    blended_bg = Image.blend(blurred_bg, black_overlay, 0.6)

    overlay_data = np.array(music_overlay.convert('RGBA'))
    r, g, b, a = overlay_data.T
    white_mask = (r == 255) & (g == 255) & (b == 255)
    overlay_data[..., :-1][white_mask.T] = make_col()
    music_overlay = Image.fromarray(overlay_data)

    min_dim = min(bg_image.size)
    left = (bg_image.width - min_dim) // 2
    top = (bg_image.height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    cropped = bg_image.crop((left, top, right, bottom)).resize((600, 600))

    circle_mask = Image.new("L", (600, 600), 0)
    ImageDraw.Draw(circle_mask).ellipse((0, 0, 600, 600), fill=255)
    cropped.putalpha(circle_mask)

    blended_bg.paste(cropped, (50, 70), mask=cropped)
    blended_bg.paste(music_overlay, (0, 0), mask=music_overlay)

    font_small = ImageFont.truetype(r"Music/core/resources/robot.otf", 30)
    font_large = ImageFont.truetype(r"Music/core/resources/robot.otf", 60)
    font_title = ImageFont.truetype(r"Music/core/resources/robot.otf", 49)
    font_info = ImageFont.truetype(r"Music/core/resources/font.ttf", 35)

    draw = ImageDraw.Draw(blended_bg)
    draw.text((10, 10), "MUSIC PLAYER", fill="white", font=font_small)
    draw.text((670, 150), "NOW PLAYING", fill="white", font=font_large, stroke_width=2, stroke_fill="white")

    title_lines = truncate(title)
    draw.text((670, 280), title_lines[0], fill="white", font=font_title)
    draw.text((670, 332), title_lines[1], fill="white", font=font_title)

    draw.text((670, 410), f"Views : {views}", fill="white", font=font_info)
    draw.text((670, 460), f"Duration : {duration} minutes", fill="white", font=font_info)
    draw.text((670, 510), f"Channel : {channel}", fill="white", font=font_info)

    blended_bg.save("final.png")
    os.remove("background.png")
    return "final.png"


