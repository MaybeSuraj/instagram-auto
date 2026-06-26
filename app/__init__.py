import env
import sys
import asyncio
from logger import LOGGER
from pathlib import Path
from pyrogram import Client
from instagrapi import Client as IGClient

loop = asyncio.get_event_loop()
botname = ""
botusername = ""

bot: Client = Client(
    "InstagramAuto",
    env.API_ID,
    env.API_HASH,
    bot_token=env.BOT_TOKEN,
    plugins=dict(root="app.plugins"),
    max_concurrent_transmissions=5,
)


igClient = IGClient()
igClient.delay_range = [
    1,
    3,
]  # Set a delay range between requests to avoid rate limiting


async def initiate_tg_bot():
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


async def initiate_ig_client():
    global igClient
    LOGGER(__name__).info("STARTING INSTAGRAM CLIENT")
    try:
        ig_setting_path = Path("instagram_settings.json")
        if ig_setting_path.exists():
            LOGGER(__name__).info("INSTAGRAM SETTINGS FOUND, LOADING SETTINGS")
            igClient.load_settings("instagram_settings.json")

        else:
            LOGGER(__name__).info("INSTAGRAM SETTINGS NOT FOUND, LOGGING IN")
            igClient.login_by_sessionid(env.INSTAGRAM_SESSION_ID)
            LOGGER(__name__).info("INSTAGRAM LOGIN SUCCESSFUL, DUMPING SETTINGS")
            igClient.dump_settings("instagram_settings.json")

    except Exception as e:
        LOGGER(__name__).error(f"\033[31m{e}")
        sys.exit(0)
    LOGGER(__name__).info("INSTAGRAM CLIENT STARTED")


loop.run_until_complete(initiate_tg_bot())
loop.run_until_complete(initiate_ig_client())
