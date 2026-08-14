import asyncio

from pyrogram import idle

from Nexa.core.assistant import assistant
from Nexa.core.bot import bot
from Nexa.core.call import call


async def main():
    print("🚀 Starting Nexa Music...")

    try:
        await bot.start()
        print("✅ Bot started")

        await assistant.start()
        print("✅ Assistant started")

        await call.start()
        print("✅ PyTgCalls started")

        print("🎵 Nexa Music is running")
        await idle()

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(f"❌ Startup error: {e}")

    finally:
        print("🛑 Stopping Nexa Music...")

        try:
            await call.stop()
        except Exception:
            pass

        try:
            await assistant.stop()
        except Exception:
            pass

        try:
            await bot.stop()
        except Exception:
            pass

        print("✅ Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())