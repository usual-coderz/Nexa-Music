import re

from pyrogram import filters
from pyrogram.types import Message

from Nexa.core.bot import bot
from Nexa.core.call import play_item
from Nexa.core.helpers import is_admin
from Nexa.core.queue import CURRENT, queue
from Nexa.youtube import YouTube, VideosSearch, download_song, download_video

URL_REGEX = r"(?:youtube\.com|youtu\.be)"


def extract_query(message: Message):
    if len(message.command) > 1:
        return message.text.split(None, 1)[1]
    if message.reply_to_message:
        rep = message.reply_to_message
        return rep.text or rep.caption
    return None


@bot.on_message(filters.command(["play", "vplay"]) & filters.group)
async def play(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply("❌ Ye command sirf **group admins** use kar sakte hain.")

    chat_id = message.chat.id
    query = extract_query(message)
    if not query:
        return await message.reply("ℹ️ Song ka naam ya YouTube link do.\nUsage: `/play <song name ya link>`")

    is_video = message.command[0].lower() == "vplay"
    msg = await message.reply("⏳ Search aur download ho raha hai...")

    if re.search(URL_REGEX, query):
        link = query
    else:
        search = VideosSearch(query, limit=1)
        result = (await search.next()).get("result") or []
        if not result:
            return await msg.edit("❌ Kuch nahi mila. Dobara try karo.")
        link = "https://www.youtube.com/watch?v=" + result[0]["id"]

    details = await YouTube.details(link)
    if not details:
        return await msg.edit("❌ Video details nahi mil payi.")
    title, duration_min, duration_sec, thumb, vidid = details

    if is_video:
        file_path = await download_video(link)
    else:
        file_path = await download_song(link)

    if not file_path:
        return await msg.edit("❌ Download fail ho gaya. Dobara try karo.")

    item = {
        "file": file_path,
        "title": title,
        "duration": duration_min,
        "is_video": is_video,
    }

    queue.add(chat_id, item)

    if chat_id in CURRENT:
        pos = queue.length(chat_id)
        return await msg.edit(
            f"✅ **{title}** queue me add ho gaya (#{pos}).\n⏱ Duration: {duration_min}"
        )

    ok = await play_item(chat_id, item)
    if ok:
        await msg.edit(
            f"▶️ **Ab play ho raha hai:** {title}\n"
            f"⏱ Duration: {duration_min}\n"
            f"🎬 Video: {'✅' if is_video else '❌'}"
        )
    else:
        queue.clear(chat_id)
        await msg.edit(
            "❌ Voice chat me join nahi ho paya.\n"
            "1. Assistant ko group me add karo\n"
            "2. Group me voice chat start karke /play do\n"
            "3. Bot + assistant dono ko admin banao"
        )