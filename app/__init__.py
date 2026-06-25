import env
import sys
from logger import LOGGER
import asyncio

from pyrogram import Client

loop = asyncio.get_event_loop()
botname = ""
botusername = ""

bot: Client = Client(
    "InstagramAuto",
    env.API_ID,
    env.API_HASH,
    bot_token=env.BOT_TOKEN,
    plugins=dict(root="app.plugins"),
)


async def initiate_bot():
    global botname, botusername
    LOGGER(__name__).info("STARTING BOT")
    try:
        await bot.start()
    except Exception as e:
        LOGGER(__name__).error(f"\033[31m{e}")
        sys.exit(0)
    getme = await bot.get_me()
    botusername = (getme.username).lower()
    if getme.last_name:
        botname = getme.first_name + " " + getme.last_name
    else:
        botname = getme.first_name
    LOGGER(__name__).info(f"BOT STARTED AS {botname}")


loop.run_until_complete(initiate_bot())
