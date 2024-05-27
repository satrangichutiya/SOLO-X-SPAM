import asyncio
from random import choice
from telethon import events
from config import X1, SUDO_USERS, OWNER_ID, CMD_HNDLR as hl
from JARVIS.data import RAID, REPLYRAID, FRIDAY, MRAID, SRAID, QRAID, FRIDAY

REPLY_RAID = []

async def get_entity_from_message(event):
    text = event.text.split(" ", 2)
    if len(text) >= 2:
        return await event.client.get_entity(text[2])
    elif event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        return await event.client.get_entity(reply_message.sender_id)
    return None

async def send_raid_message(event, raid_list, counter, entity):
    first_name = entity.first_name
    uid = entity.id
    username = f"[{first_name}](tg://user?id={uid})"
    for _ in range(counter):
        reply = choice(raid_list)
        caption = f"{username} {reply}"
        await event.client.send_message(event.chat_id, caption)
        await asyncio.sleep(0.1)

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sraid(?: |$)(.*)" % hl))
async def raid(event):
    if event.sender_id in SUDO_USERS:
        entity = await get_entity_from_message(event)
        if entity:
            try:
                counter = int(event.text.split(" ", 2)[1])
                await send_raid_message(event, RAID, counter, entity)
            except (IndexError, ValueError, NameError):
                await event.reply(f"𝗠𝗼𝗱𝘂𝗹𝗲 𝗡𝗮𝗺𝗲: 𝐑𝐚𝐢𝐝\n  » {hl}raid <ᴄᴏᴜɴᴛ> <ᴜꜱᴇʀɴᴀᴍᴇ ᴏꜰ ᴜꜱᴇʀ>\n  » {hl}raid <ᴄᴏᴜɴᴛ> <ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ>")

@X1.on(events.NewMessage(incoming=True, pattern=r"\%srraid(?: |$)(.*)" % hl))
async def rraid(event):
    if event.sender_id in SUDO_USERS:
        entity = await get_entity_from_message(event)
        if entity:
            check = f"{entity.id}_{event.chat_id}"
            global REPLY_RAID
            if check in REPLY_RAID:
                REPLY_RAID.remove(check)
            await event.reply("» HAT GYA REPLY RAID !! ✅")

@X1.on(events.NewMessage(incoming=True))
async def _(event):
    global REPLY_RAID
    check = f"{event.sender_id}_{event.chat_id}"
    if check in REPLY_RAID:
        await event.client.send_message(
            entity=event.chat_id,
            message="""{}""".format(choice(REPLYRAID)),
            reply_to=event.message.id,
        )
        await asyncio.sleep(0.1)


async def get_entity_from_message(event):
    text = event.text.split(" ", 2)
    if len(text) >= 2:
        return await event.client.get_entity(text[2])
    elif event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        return await event.client.get_entity(reply_message.sender_id)
    return None

async def send_raid_message(event, raid_list, counter, entity):
    first_name = entity.first_name
    uid = entity.id
    username = f"[{first_name}](tg://user?id={uid})"
    for _ in range(counter):
        reply = choice(raid_list)
        caption = f"{username} {reply}"
        await event.client.send_message(event.chat_id, caption)
        await asyncio.sleep(0.1)

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sdrraid(?: |$)(.*)" % hl))
async def drraid(event):
    if event.sender_id in SUDO_USERS:
        entity = await get_entity_from_message(event)
        if entity:
            check = f"{entity.id}_{event.chat_id}"
            global REPLY_RAID
            if check in REPLY_RAID:
                REPLY_RAID.remove(check)
            await event.reply("» HAT GYA REPLY RAID !! ✅")

@X1.on(events.NewMessage(incoming=True, pattern=r"\%smraid(?: |$)(.*)" % hl))
async def mraid(event):
    if event.sender_id in SUDO_USERS:
        entity = await get_entity_from_message(event)
        if entity:
            try:
                counter = int(event.text.split(" ", 2)[1])
                await send_raid_message(event, MRAID, counter, entity)
            except (IndexError, ValueError, NameError):
                await event.reply(f"𝗠𝗼𝗱𝘂𝗹𝗲 𝗡𝗮𝗺𝗲: 𝗠𝗥𝗮𝗶𝗱\n  » {hl}mraid <ᴄᴏᴜɴᴛ> <ᴜꜱᴇʀɴᴀᴍᴇ ᴏꜰ ᴜꜱᴇʀ>\n  » {hl}mraid <ᴄᴏᴜɴᴛ> <ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ>")

@X1.on(events.NewMessage(incoming=True, pattern=r"\%ssraid(?: |$)(.*)" % hl))
async def sraid(event):
    if event.sender_id in SUDO_USERS:
        entity = await get_entity_from_message(event)
        if entity:
            try:
                counter = int(event.text.split(" ", 2)[1])
                await send_raid_message(event, SRAID, counter, entity)
            except (IndexError, ValueError, NameError):
                await event.reply(f"𝗠𝗼𝗱𝘂𝗹𝗲 𝗡𝗮𝗺𝗲: 𝗦𝗥𝗮𝗶𝗱\n  » {hl}sraid <ᴄᴏᴜɴᴛ> <ᴜꜱᴇʀɴᴀᴍᴇ ᴏꜰ ᴜꜱᴇʀ>\n  » {hl}sraid <ᴄᴏᴜɴᴛ> <ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ>")

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sqraid(?: |$)(.*)" % hl))
async def qraid(event):
    if event.sender_id in SUDO_USERS:
        entity = await get_entity_from_message(event)
        if entity:
            try:
                counter = int(event.text.split(" ", 2)[1])
                await send_raid_message(event, QRAID, counter, entity)
            except (IndexError, ValueError, NameError):
                await event.reply(f"𝗠𝗼𝗱𝘂𝗹𝗲 𝗡𝗮𝗺𝗲: 𝐐𝐑𝐚𝐢𝐝\n  » {hl}raid <ᴄᴏᴜɴᴛ> <ᴜꜱᴇʀɴᴀᴍᴇ ᴏꜰ ᴜꜱᴇʀ>\n  » {hl}raid <ᴄᴏᴜɴᴛ> <ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ>")
