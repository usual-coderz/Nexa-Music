# gen_string.py
import asyncio

from pyrogram import Client

API_ID = int(input("API_ID: "))
API_HASH = input("API_HASH: ")


async def main():
    async with Client("session_gen", api_id=API_ID, api_hash=API_HASH) as app:
        s = await app.export_session_string()
        print("\nSTRING_SESSION (ye .env me daalo):\n")
        print(s)


asyncio.run(main())