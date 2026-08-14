import os
import re
from typing import Union

import aiohttp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

try:
    from py_yt import VideosSearch, Playlist
except ImportError:
    from youtube_search import VideosSearch, Playlist

from Nexa import config

DOWNLOAD_DIR = config.DOWNLOAD_DIR


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


async def download_song(link: str) -> str:
    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
    if not video_id or len(video_id) < 3:
        return None

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{config.NEXA_API_URL}/download",
                params={"url": video_id, "type": "audio", "api_key": config.NEXA_API_KEY},
                timeout=aiohttp.ClientTimeout(total=300),
            ) as resp:
                if resp.status != 200:
                    return None
                with open(file_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(131072):
                        f.write(chunk)
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return file_path
        return None
    except Exception:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        return None


async def download_video(link: str) -> str:
    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link
    if not video_id or len(video_id) < 3:
        return None

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{config.NEXA_API_URL}/download",
                params={"url": video_id, "type": "video", "api_key": config.NEXA_API_KEY},
                timeout=aiohttp.ClientTimeout(total=600),
            ) as resp:
                if resp.status != 200:
                    return None
                with open(file_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(131072):
                        f.write(chunk)
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return file_path
        return None
    except Exception:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        return None


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def _clean(self, link: str, videoid=None) -> str:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if re.search(self.regex, link):
            if "watch?v=" in link:
                link = link.split("watch?v=")[-1].split("&")[0]
            elif "youtu.be/" in link:
                link = link.split("youtu.be/")[-1].split("?")[0]
        return link

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset: entity.offset + entity.length]
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        link = self._clean(link, videoid)
        results = VideosSearch(link, limit=1)
        data = (await results.next()).get("result") or []
        if not data:
            return None
        result = data[0]
        title = result["title"]
        duration_min = result["duration"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        vidid = result["id"]
        duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        link = self._clean(link, videoid)
        results = VideosSearch(link, limit=1)
        data = (await results.next()).get("result") or []
        return data[0]["title"] if data else None

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        link = self._clean(link, videoid)
        results = VideosSearch(link, limit=1)
        data = (await results.next()).get("result") or []
        return data[0]["duration"] if data else None

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        link = self._clean(link, videoid)
        results = VideosSearch(link, limit=1)
        data = (await results.next()).get("result") or []
        return data[0]["thumbnails"][0]["url"].split("?")[0] if data else None

    async def video(self, link: str, videoid: Union[bool, str] = None):
        link = self._clean(link, videoid)
        try:
            downloaded_file = await download_video(link)
            if downloaded_file:
                return 1, downloaded_file
            return 0, "Video download failed"
        except Exception as e:
            return 0, f"Video download error: {e}"

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            plist = await Playlist.get(link)
        except Exception:
            return []
        videos = plist.get("videos") or []
        ids = []
        for data in videos[:limit]:
            if not data:
                continue
            vid = data.get("id")
            if vid:
                ids.append(vid)
        return ids

    async def track(self, link: str, videoid: Union[bool, str] = None):
        link = self._clean(link, videoid)
        results = VideosSearch(link, limit=1)
        data = (await results.next()).get("result") or []
        if not data:
            return None, None
        result = data[0]
        track_details = {
            "title": result["title"],
            "link": result["link"],
            "vidid": result["id"],
            "duration_min": result["duration"],
            "thumb": result["thumbnails"][0]["url"].split("?")[0],
        }
        return track_details, result["id"]

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        link = self._clean(link, videoid)
        ytdl_opts = {"quiet": True}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    if "dash" not in str(format["format"]).lower():
                        formats_available.append(
                            {
                                "format": format["format"],
                                "filesize": format.get("filesize"),
                                "format_id": format["format_id"],
                                "ext": format["ext"],
                                "format_note": format["format_note"],
                                "yturl": link,
                            }
                        )
                except Exception:
                    continue
        return formats_available, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        link = self._clean(link, videoid)
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result") or []
        if not result or query_type >= len(result):
            return None
        r = result[query_type]
        return r["title"], r["duration"], r["thumbnails"][0]["url"].split("?")[0], r["id"]

    async def download(self, link: str, video: Union[bool, str] = None, videoid: Union[bool, str] = None):
        link = self._clean(link, videoid)
        try:
            if video:
                f = await download_video(link)
            else:
                f = await download_song(link)
            return (f, True) if f else (None, False)
        except Exception:
            return None, False


YouTube = YouTubeAPI()