from pytgcalls import PyTgCalls
from pytgcalls.types import AudioQuality, MediaStream, VideoQuality

from Nexa.core.assistant import assistant
from Nexa.core.queue import CURRENT, queue

call = PyTgCalls(assistant)


async def play_item(chat_id: int, item: dict) -> bool:
    CURRENT[chat_id] = item
    try:
        if item.get("is_video"):
            stream = MediaStream(
                item["file"],
                audio_flags=AudioQuality.HIGH,
                video_flags=VideoQuality.SD_480p,
            )
        else:
            stream = MediaStream(item["file"], audio_flags=AudioQuality.HIGH)
        await call.play(chat_id, stream)
        return True
    except Exception as e:
        print("play error:", e)
        CURRENT.pop(chat_id, None)
        return False


async def play_next(chat_id: int):
    item = queue.next(chat_id)
    if not item:
        CURRENT.pop(chat_id, None)
        return
    await play_item(chat_id, item)


@call.on_stream_end()
async def on_stream_end(client, update):
    chat_id = update.chat_id
    loop_state = queue.get_loop(chat_id)
    current = CURRENT.get(chat_id)

    if current and loop_state["enabled"]:
        if loop_state["count"]:
            loop_state["count"] -= 1
            if loop_state["count"] <= 0:
                queue.set_loop(chat_id, False, 0)
        await play_item(chat_id, current)
        return

    await play_next(chat_id)