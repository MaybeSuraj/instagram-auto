from pyrogram import filters, Client


@Client.on_message(filters=[filters.command("start")])
async def start(client, message):
    await message.reply_text(
        f"Hello {message.from_user.first_name}!\n\nI am a bot that can help you automate your Instagram account.\n\nUse /help to see what I can do."
    )
