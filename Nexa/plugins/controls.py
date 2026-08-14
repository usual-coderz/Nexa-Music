from pyrogram import filters
from pyrogram.types import Message

from Nexa.core.bot import bot
from Nexa.core.call import call
from Nexa.core.helpers import is_admin
from Nexa.core.queue import CURRENT, queue


@bot.on_message(filters.command("pause") & filters.group)
async def pause(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply("❌ Sirf admins.")
    chat_id = message.chat.id
    if chat_id not in CURRENT:
        return await message.reply("ℹ️ Kuch play nahi ho raha.")
    await call.pause_stream(chat_id)
    await message.reply("⏸️ Pause kar diya.")


@bot.on_message(filters.command("resume") & filters.group)
async def resume(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply("❌ Sirf admins.")
    chat_id = message.chat.id
    if chat_id not in CURRENT:
        return await message.reply("ℹ️ Kuch play nahi ho raha.")
    await call.resume_stream(chat_id)
    await message.reply("▶️ Resume ho gaya.")


@bot.on_message(filters.command("stop") & filters.group)
async def stop(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply("❌ Sirf admins.")
    chat_id = message.chat.id
    queue.clear(chat_id)
    queue.set_loop(chat_id, False, 0)
    CURRENT.pop(chat_id, None)
    try:
        await call.leave_call(chat_id)
    except Exception:
        pass
    await message.reply("⏹️ Playback band, queue clear.")