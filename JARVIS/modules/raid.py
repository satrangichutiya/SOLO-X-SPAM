import asyncio
from random import choice
from telethon import events
from config import X1, SUDO_USERS, OWNER_ID, CMD_HNDLR as hl
from JARVIS.data import RAID, REPLYRAID, FRIDAY, MRAID, SRAID, QRAID

REPLY_RAID = []

# Helper function to get user entity from a message
async def get_user_entity(e):
    if len(e.text.split()) > 2:
        return await e.client.get_entity(e.text.split()[2])
    if e.reply_to_msg_id:
        reply_msg = await e.get_reply_message()
        return await e.client.get_entity(reply_msg.sender_id)
    return None

# Helper function to handle exceptions
async def handle_exception(e, module_name):
    if not (e.reply_to_msg_id or len(e.text.split()) > 2):
        await e.reply(f"𝗠𝗼𝗱𝘂𝗹𝗲 𝗡𝗮𝗺𝗲: {module_name}\n  » {hl}{module_name.lower()} <ᴄᴏᴜɴᴛ> <ᴜꜱᴇʀɴᴀᴍᴇ ᴏꜰ ᴜꜱᴇʀ>\n  » {hl}{module_name.lower()} <ᴄᴏᴜɴᴛ> <ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ>")

# Function to execute raid
async def execute_raid(e, uid, first_name, counter, raid_list):
    username = f"[{first_name}](tg://user?id={uid})"
    for _ in range(counter):
        reply = choice(raid_list)
        caption = f"{username} {reply}"
        await e.client.send_message(e.chat_id, caption)
        await asyncio.sleep(0.1)

# Event handler for different raid types
async def raid_handler(e, raid_list, module_name):
    if e.sender_id in SUDO_USERS:
        try:
            entity = await get_user_entity(e)
            if entity:
                uid = entity.id
                first_name = entity.first_name
                counter = int(e.text.split()[1])
                if uid in FRIDAY:
                    await e.reply("REPO OWNER HAI YE.")
                elif uid == OWNER_ID:
                    await e.reply("BETA BAAP PE RAID NHI KRTE HAI...")
                elif uid in SUDO_USERS:
                    await e.reply("YE BHI JARVIS KA BACHA HAI ISPE RAID MAT MARO!...")
                else:
                    await execute_raid(e, uid, first_name, counter, raid_list)
            else:
                await handle_exception(e, module_name)
        except (IndexError, ValueError, NameError):
            await handle_exception(e, module_name)
        except Exception as ex:
            print(ex)

# Event handler for reply raid
async def reply_raid_handler(e, module_name):
    if e.sender_id in SUDO_USERS:
        try:
            entity = await get_user_entity(e)
            if entity:
                user_id = entity.id
                if user_id in FRIDAY:
                    await e.reply("Beta Repo Owner Hai ye , Gand Me Lund Daalke chla dega...")
                elif user_id == OWNER_ID:
                    await e.reply("Beta Dobara Kiya Nah Toh Jha se Nikle ho Whi Gaad diye jaoge🥱...")
                elif user_id in SUDO_USERS:
                    await e.reply("YE BHI JARVIS KA BACHA HAI ISPE RAID MAT MARO!...")
                else:
                    check = f"{user_id}_{e.chat_id}"
                    if check not in REPLY_RAID:
                        REPLY_RAID.append(check)
                    await e.reply("» LAG GYA REPLY RAID.. !! ✅")
            else:
                await handle_exception(e, module_name)
        except NameError:
            await handle_exception(e, module_name)

# Event handler for disabling reply raid
async def disable_reply_raid_handler(e, module_name):
    if e.sender_id in SUDO_USERS:
        try:
            entity = await get_user_entity(e)
            if entity:
                check = f"{entity.id}_{e.chat_id}"
                if check in REPLY_RAID:
                    REPLY_RAID.remove(check)
                await e.reply("» HAT GYA REPLY RAID !! ✅")
            else:
                await handle_exception(e, module_name)
        except NameError:
            await handle_exception(e, module_name)

# Adding event handlers
@X1.on(events.NewMessage(incoming=True, pattern=rf"\%sraid(?: |$)(.*)" % hl))
async def raid_event(e):
    await raid_handler(e, RAID, "Raid")

@X1.on(events.NewMessage(incoming=True))
async def reply_raid_event(event):
    check = f"{event.sender_id}_{event.chat_id}"
    if check in REPLY_RAID:
        await asyncio.sleep(0.1)
        await event.client.send_message(
            entity=event.chat_id,
            message=choice(REPLYRAID),
            reply_to=event.message.id,
        )

@X1.on(events.NewMessage(incoming=True, pattern=rf"\%srraid(?: |$)(.*)" % hl))
async def rraid_event(e):
    await reply_raid_handler(e, "ReplyRaid")

@X1.on(events.NewMessage(incoming=True, pattern=rf"\%sdrraid(?: |$)(.*)" % hl))
async def drraid_event(e):
    await disable_reply_raid_handler(e, "DRreplyRaid")

@X1.on(events.NewMessage(incoming=True, pattern=rf"\%smraid(?: |$)(.*)" % hl))
async def mraid_event(e):
    await raid_handler(e, MRAID, "MRaid")

@X1.on(events.NewMessage(incoming=True, pattern=rf"\%ssraid(?: |$)(.*)" % hl))
async def sraid_event(e):
    await raid_handler(e, SRAID, "SRaid")

@X1.on(events.NewMessage(incoming=True, pattern=rf"\%sqraid(?: |$)(.*)" % hl))
async def qraid_event(e):
    await raid_handler(e, QRAID, "QRaid")
