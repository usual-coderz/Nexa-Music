from pyrogram import Client

from Nexa import config

bot = Client(
    "NexaMusicBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="Nexa/plugins"),
)