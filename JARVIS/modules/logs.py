import asyncio
import heroku3
from pymongo import MongoClient
from config import X1, SUDO_USERS, OWNER_ID, HEROKU_API_KEY, HEROKU_APP_NAME, CMD_HNDLR as hl
from datetime import datetime
from telethon import events
from telethon.errors import ForbiddenError

async def fetch_heroku_logs(ANNIE):
    if (HEROKU_APP_NAME is None) or (HEROKU_API_KEY is None):
        await ANNIE.reply(
            "First Set These Vars In Heroku: `HEROKU_API_KEY` And `HEROKU_APP_NAME`.",
        )
        return None

    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        await ANNIE.reply(
            "Make Sure Your Heroku API Key & App Name Are Configured Correctly In Heroku."
        )
        return None

    return app.get_log()

async def write_logs_to_file(logs):
    with open("JARVISlogs.txt", "w") as logfile:
        logfile.write("⚡ JARVISBOTS ⚡ [ Bot Logs ]\n\n" + logs)

async def send_logs_file(ANNIE, ms):
    try:
        await X1.send_file(ANNIE.chat_id, "JARVISlogs.txt", caption=f"⚡ **JARVIS BOTS LOGS** ⚡\n  » **Time Taken:** `{ms} seconds`")
    except Exception as e:
        await ANNIE.reply(f"An Exception Occurred!\n\n**ERROR:** {str(e)}")

@X1.on(events.NewMessage(incoming=True, pattern=r"\%slogs(?: |$)(.*)" % hl))
async def logs(ANNIE):
    if ANNIE.sender_id == OWNER_ID:
        start = datetime.now()
        fetch = await ANNIE.reply(f"__Fetching Logs...__")
        logs = await fetch_heroku_logs(ANNIE)

        if logs is not None:
            await write_logs_to_file(logs)
            end = datetime.now()
            ms = (end - start).seconds
            await asyncio.sleep(1)
            await send_logs_file(ANNIE, ms)
            await fetch.delete()

    elif ANNIE.sender_id in SUDO_USERS:
        await ANNIE.reply("» BSDK..ISKO SIRF OWNER USE KR SKTA HAI...")
