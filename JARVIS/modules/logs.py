import asyncio
import heroku3
from pymongo import MongoClient
from config import X1, SUDO_USERS, OWNER_ID, HEROKU_API_KEY, HEROKU_APP_NAME, CMD_HNDLR as hl
from datetime import datetime
from telethon import events
from telethon.errors import ForbiddenError
from telethon.tl.custom import Button

# MongoDB configuration
MONGO_URI = 'mongodb+srv://JARVIS:SPAMX10@jarvisspam.2wmzbix.mongodb.net/?retryWrites=true&w=majority&appName=JarvisSpam'
client = MongoClient(MONGO_URI)
db = client['bot_database']
stats_collection = db['stats']

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

@X1.on(events.NewMessage(incoming=True))
async def track_stats(event):
    if event.is_group:
        group_id = event.chat_id
        stats_collection.update_one(
            {'type': 'group', 'id': group_id},
            {'$set': {'id': group_id}},
            upsert=True
        )
    if event.is_private:
        user_id = event.sender_id
        stats_collection.update_one(
            {'type': 'user', 'id': user_id}},
            {'$set': {'id': user_id}},
            upsert=True
        )

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sstats(?: |$)(.*)" % hl))
async def check_stats(event):
    if event.sender_id == OWNER_ID:
        buttons = [
            [Button.inline("User Stats", data="user_stats")],
            [Button.inline("Group Stats", data="group_stats")],
            [Button.inline("Overall Stats", data="overall_stats")]
        ]
        await event.reply("Choose the stats you want to view:", buttons=buttons)
    else:
        await event.reply("You do not have permission to use this command.")

@X1.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode('utf-8')
    if data == "user_stats":
        user_count = stats_collection.count_documents({'type': 'user'})
        await event.edit(f"Total Users: {user_count}")
    elif data == "group_stats":
        group_count = stats_collection.count_documents({'type': 'group'})
        await event.edit(f"Total Groups: {group_count}")
    elif data == "overall_stats":
        user_count = stats_collection.count_documents({'type': 'user'})
        group_count = stats_collection.count_documents({'type': 'group'})
        await event.edit(f"Total Users: {user_count}\nTotal Groups: {group_count}")

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sbroadcast(?: |$)(.*)" % hl))
async def broadcast(event):
    if event.sender_id == OWNER_ID:
        reply = await event.get_reply_message()
        message = event.pattern_match.group(1) or (reply and reply.text)

        if not message:
            await event.reply("Please provide a message to broadcast or reply to a message.")
            return
        
        users = stats_collection.find({'type': 'user'})
        groups = stats_collection.find({'type': 'group'})
        
        for user in users:
            try:
                await X1.send_message(user['id'], message)
            except ForbiddenError:
                pass  # Ignore if the bot is blocked
            except Exception as e:
                print(f"Error sending message to {user['id']}: {str(e)}")
        
        for group in groups:
            try:
                await X1.send_message(group['id'], message)
            except ForbiddenError:
                pass  # Ignore if the bot is removed from the group
            except Exception as e:
                print(f"Error sending message to {group['id']}: {str(e)}")
        
        await event.reply("Broadcast completed.")
    else:
        await event.reply("You do not have permission to use this command.")
