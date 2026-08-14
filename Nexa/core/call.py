from pytgcalls import PyTgCalls
from pytgcalls import filters as tg_filters
from pytgcalls.types import AudioQuality
from pytgcalls.types import MediaStream
from pytgcalls.types import StreamEnded
from pytgcalls.types import VideoQuality

from Nexa.core.assistant import assistant
from Nexa.core.queue import CURRENT, queue


call = PyTgCalls(assistant)


async def play_item(chat_id: int, item: dict) -> bool:
    CURRENT[chat_id] = item

    try:
        if item.get("is_video"):
            stream = MediaStream(
                item["file"],
                AudioQuality.HIGH,
                VideoQuality.SD_480p,
            )
        else:
            stream = MediaStream(
                item["file"],
                audio_flags=AudioQuality.HIGH,
                video_flags=MediaStream.Flags.IGNORE,
            )

        await call.play(chat_id, stream)
        return True

    except Exception as e:
        print(f"❌ Play error [{chat_id}]: {e}")
        CURRENT.pop(chat_id, None)
        return False


async def play_next(chat_id: int):
    item = queue.next(chat_id)

    if not item:
        CURRENT.pop(chat_id, None)
        return False

    return await play_item(chat_id, item)


@call.on_update(tg_filters.stream_end())
async def on_stream_end(
    _,
    update: StreamEnded,
):
    chat_id = update.chat_id

    current = CURRENT.get(chat_id)
    if not current:
        await play_next(chat_id)
        return

    loop_state = queue.get_loop(chat_id)

    if loop_state["enabled"]:
        count = loop_state.get("count", 0)

        if count:
            count -= 1
            loop_state["count"] = count

            if count <= 0:
                queue.set_loop(chat_id, False, 0)

        # Loop current item
        if loop_state["enabled"]:
            await play_item(chat_id, current)
            return

    # Normal queue playback
    await play_next(chat_id)