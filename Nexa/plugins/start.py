from pyrogram import filters
from pyrogram.types import Message

from Nexa.core.bot import bot

HELP_TEXT = """
🎵 **Nexa Music Bot**

Commands (sirf **group admins**):
• `/play <song name ya link>` — audio play karo
• `/vplay <song name ya link>` — video play karo
• `/pause` — pause
• `/resume` — resume
• `/stop` — band + queue clear
• `/loop` — loop toggle (infinite)
• `/loop 2` — 2 baar repeat
• `/loop enable` / `/loop disable`

💡 **Note:** Group me voice chat pehle start karo, aur bot + assistant dono ko admin banao.
"""


@bot.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply("👋 Hello! Main ek VC music bot hoon. Mujhe group me add karo aur /play use karo.")


@bot.on_message(filters.command("help"))
async def help_cmd(client, message: Message):
    await message.reply(HELP_TEXT)