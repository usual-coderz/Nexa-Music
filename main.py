import asyncio

from pyrogram import idle

from Nexa.core.assistant import assistant
from Nexa.core.bot import bot
from Nexa.core.call import call


async def main():
    print("Starting bot...")
    await bot.start()
    print("✅ Bot client started")

    await assistant.start()
    print("✅ Assistant started")

    await call.start()
    print("✅ PyTgCalls started")

    await idle()

    print("Stopping...")
    await call.stop()
    await assistant.stop()
    await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())