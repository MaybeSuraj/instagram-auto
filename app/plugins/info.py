import env
from pyrogram import Client, filters
from app import igClient
from app.utils import INSTAGRAM_URL_RE


@Client.on_message(filters.command("info") & filters.private & env.owner_filter)
async def handle_info(client: Client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a URL.")
        return

    video_url = message.command[1].strip()
    if not INSTAGRAM_URL_RE.search(video_url):
        await message.reply_text("Please provide a valid Instagram reel or post URL.")
        return

    try:
        replied_message = await message.reply_text("Fetching video info...")
        media_pk = igClient.media_pk_from_url(video_url)
        media_info = igClient.media_info_v1(media_pk)

        info_text = "** Info:**\n\n"
        info_text += f"**ID:** {media_info.pk}\n"
        info_text += f"**Type:** {media_info.media_type}\n"
        info_text += f"**Caption:** {media_info.caption_text}\n"
        info_text += f"**Likes:** {media_info.like_count}\n"
        info_text += f"**Comments:** {media_info.comment_count}\n"
        info_text += f"**Views:** {media_info.view_count}\n"
        info_text += f"**Posted at:** {media_info.taken_at}\n"

        await replied_message.edit_text(info_text)
    except Exception as e:
        await message.reply_text(
            f"An error occurred while fetching video info: {str(e)}"
        )
