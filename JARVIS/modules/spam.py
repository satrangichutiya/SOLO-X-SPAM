## Copy Paster Must Give Credit...
## @JARVIS_V2

import asyncio
from random import choice
from telethon import events, functions, types
from JARVIS.data import GROUP, PORMS
from config import X1, SUDO_USERS, CMD_HNDLR as hl

async def gifspam(event, message):
    try:
        await event.client(
            functions.messages.SaveGifRequest(
                id=types.InputDocument(
                    id=message.media.document.id,
                    access_hash=message.media.document.access_hash,
                    file_reference=message.media.document.file_reference,
                ),
                unsave=True,
            )
        )
    except Exception:
        pass

async def send_messages(event, message, count):
    for _ in range(count):
        if event.reply_to_msg_id:
            await event.reply(message)
        else:
            await event.client.send_message(event.chat_id, message)
        await asyncio.sleep(0.2)

async def send_media(event, message, count):
    for _ in range(count):
        message = await event.client.send_file(event.chat_id, message, caption=message.text)
        await gifspam(event, message)
        await asyncio.sleep(0.2)

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sspam(?: |$)(.*)" % hl))
async def spam(event):
    if event.sender_id in SUDO_USERS:
        command = event.text.split(" ", 2)
        reply_message = await event.get_reply_message()
        try:
            count = int(command[1])
            if len(command) == 3:
                await send_messages(event, command[2], count)
            elif reply_message.media:
                await send_media(event, reply_message, count)
            elif reply_message.text:
                await send_messages(event, reply_message.text, count)
            else:
                await event.reply(f"⚔️ **ᴜsᴀɢᴇ:**\n  » {hl}spam 04 ᴊᴀʀᴠɪs\n  » {hl}spam 04 <ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ>\n\n**ᴛᴏ ᴅᴏ sᴘᴀᴍ ᴡɪᴛʜ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴜsᴇʀ:**\n  » {hl}spam 04 ᴊᴀʀᴠɪs <ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ>")
        except (IndexError, ValueError):
            await event.reply(f"⚔️ **ᴜsᴀɢᴇ:**\n  » {hl}spam 04 ᴊᴀʀᴠɪs\n  » {hl}spam 04 <ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ>\n\n**ᴛᴏ ᴅᴏ sᴘᴀᴍ ᴡɪᴛʜ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴜsᴇʀ:**\n  » {hl}spam 04 ᴊᴀʀᴠɪs <ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ>")
        except Exception as e:
            print(e)

@X1.on(events.NewMessage(incoming=True, pattern=r"\%spspam(?: |$)(.*)" % hl))
async def pspam(event):
    if event.sender_id in SUDO_USERS:
        if event.chat_id in GROUP:
            await event.reply("➪ ᴛʜɪs ɢʀᴏᴜᴘ ɪs ɪɴ sᴜʀᴠɪʟʟᴀɴᴄᴇ ᴏғ ᴊᴀʀᴠɪs sᴏ ʜᴇʀᴇ ᴘsᴘᴀᴍ ᴡɪʟʟ ɴᴏᴛ ᴡᴏʀᴋ...")
        else:
            try:
                count = int(event.text.split(" ", 2)[1])
                porn = choice(PORMS)
                await send_media(event, porn, count)
            except (IndexError, ValueError):
                await event.reply(f"🔞 **Usage:**  {hl}pspam 04")
            except Exception as e:
                print(e)
