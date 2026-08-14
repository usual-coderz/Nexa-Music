from pyrogram import Client

from Nexa import config

assistant = Client(
    "NexaAssistant",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION,
)