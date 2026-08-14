from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from Nexa import config


async def is_admin(client, message: Message) -> bool:
    user = message.from_user
    if not user:
        return False
    if user.id == config.OWNER_ID:
        return True
    try:
        member = await client.get_chat_member(message.chat.id, user.id)
        return member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)
    except Exception:
        return False