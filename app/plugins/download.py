import env
from contextlib import suppress
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import Message
from app.utils import make_progress_callback, download_reel, INSTAGRAM_URL_RE


@Client.on_message(filters.command("download") & filters.private & env.owner_filter)
async def handle_message(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a video URL.")
        return

    video_url: str = message.command[1].strip()
    if not INSTAGRAM_URL_RE.search(video_url):
        await message.reply_text("Please provide a valid Instagram reel or post URL.")
        return

    downloaded_file = None
    try:
        replied_message = await message.reply_text("Downloading video...")
        media_info, downloaded_file = await download_reel(
            video_url,
            Path("downloads"),
        )

        await replied_message.edit_text(
            "Video downloaded successfully. Sending it back to you..."
        )

        # Send the downloaded video back to the user
        await client.send_video(
            message.chat.id,
            downloaded_file,
            progress=make_progress_callback(replied_message, "Uploading video..."),
            caption=media_info.caption_text[0:1023]
            or "Here is your downloaded video.",  # Limit caption to 1024 characters
        )
        with suppress(Exception):
            await replied_message.delete()

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
    finally:
        if downloaded_file is not None:
            Path(downloaded_file).unlink(
                missing_ok=True
            )  # Delete the downloaded video file after sending it
