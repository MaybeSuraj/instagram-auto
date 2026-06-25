import uvloop
from pyrogram import idle
from logger import LOGGER
from app import bot, botname, loop


uvloop.install()


async def initiate_bot():
    LOGGER(__name__).info("Starting Bot")
    await idle()
    await bot.stop()
    LOGGER(__name__).info(f"{botname} IS STOPPED")


if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
    LOGGER(__name__).info(f"{botname} IS STOPPED")
