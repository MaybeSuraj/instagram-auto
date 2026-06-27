import env
from contextlib import suppress
from pyrogram import Client, filters
from pyrogram.types import Message
from pathlib import Path
from typing import Optional

from app import igClient
from app.utils import INSTAGRAM_URL_RE, download_reel, make_progress_callback
from app.utils.instagram import _call_ig_client


def extract_instagram_url(message: Message) -> Optional[str]:
    if len(message.command) < 2:
        return None

    match = INSTAGRAM_URL_RE.search(message.command[1])
    return match.group(1) if match else None


@Client.on_message(filters.command("upload") & filters.private & env.owner_filter)
async def handle_upload(client: Client, message: Message):
    replied_video = message.reply_to_message
    reel_url = extract_instagram_url(message)
    video_path = None
    caption = ""
    sending_message = None

    if not replied_video and not reel_url:
        await message.reply_text(
            "Please reply to a video message or provide an Instagram reel link to upload."
        )
        return

    try:
        sending_message = await message.reply_text("Downloading video...")

        if replied_video:
            has_video = replied_video.video is not None
            has_video_document = (
                replied_video.document
                and replied_video.document.mime_type.startswith("video/")
            )

            if not (has_video or has_video_document):
                await sending_message.edit_text(
                    "The replied message is not a valid video."
                )
                return

            if replied_video.video and replied_video.video.duration > 90:
                await sending_message.edit_text(
                    "The video duration exceeds the 90 seconds limit for Instagram uploads."
                )
                return

            video_path = await replied_video.download(
                progress=make_progress_callback(sending_message, sending_message.text)
            )
            caption = replied_video.caption or ""
        else:
            await sending_message.edit_text("Downloading reel from link...")
            try:
                media_info, video_path = await download_reel(reel_url)
                caption = getattr(media_info, "caption_text", "") or ""
                duration = getattr(media_info, "video_duration", None)
            except Exception as exc:
                await sending_message.edit_text(f"Failed to download reel: {exc}")
                return

            if duration and duration > 90:
                await sending_message.edit_text(
                    "The reel duration exceeds the 90 seconds limit for Instagram uploads."
                )
                return

        await sending_message.edit_text("Uploading video to Instagram...")

        # video_upload is entirely synchronous (HTTP POST + time.sleep loops).
        # Running it directly on the event loop would block Pyrogram's
        # ping_worker for 30+ seconds, causing Telegram to drop the connection.
        uploaded_media = await _call_ig_client(
            igClient.video_upload,
            video_path,
            caption=caption[:1024],
        )

        await sending_message.edit_text(
            f"Video uploaded successfully!\n\n"
            f"**Media ID:** {uploaded_media.pk}\n"
            f"**Media URL:** https://instagram.com/p/{uploaded_media.code}\n"
        )
    finally:
        if video_path is not None:
            with suppress(Exception):
                video_file = Path(video_path)
                thumbnail_file = Path(f"{video_file}.jpg")
                video_file.unlink(missing_ok=True)
                thumbnail_file.unlink(missing_ok=True)
