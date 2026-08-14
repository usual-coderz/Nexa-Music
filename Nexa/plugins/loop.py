from pyrogram import filters
from pyrogram.types import Message

from Nexa.core.bot import bot
from Nexa.core.helpers import is_admin
from Nexa.core.queue import queue


@bot.on_message(filters.command("loop") & filters.group)
async def loop(client, message: Message):
    if not await is_admin(client, message):
        return await message.reply("❌ Sirf admins.")

    chat_id = message.chat.id
    parts = message.text.split(None, 1)
    val = parts[1].strip().lower() if len(parts) > 1 else None

    if val is None:
        cur = queue.get_loop(chat_id)
        queue.set_loop(chat_id, not cur["enabled"], 0)
        state = "ON" if not cur["enabled"] else "OFF"
        return await message.reply(f"🔁 Loop **{state}** (infinite repeat).")

    if val in ("enable", "on", "yes"):
        queue.set_loop(chat_id, True, 0)
        return await message.reply("🔁 Loop **enable** (infinite repeat).")

    if val in ("disable", "off", "no"):
        queue.set_loop(chat_id, False, 0)
        return await message.reply("🔁 Loop **disable**.")

    if val.isdigit():
        n = int(val)
        if n <= 0:
            return await message.reply("ℹ️ Positive number do.")
        queue.set_loop(chat_id, True, n)
        return await message.reply(f"🔁 Loop **{n} baar** chale ga.")

    return await message.reply("ℹ️ Usage: `/loop` | `/loop enable` | `/loop disable` | `/loop 2`")