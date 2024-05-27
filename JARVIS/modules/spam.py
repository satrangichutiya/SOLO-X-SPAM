import asyncio
from random import choice
from telethon import events, functions, types
from JARVIS.data import GROUP, PORMS
from config import X1, SUDO_USERS, CMD_HNDLR as hl

async def gifspam(e, smex):
    try:
        await e.client(
            functions.messages.SaveGifRequest(
                id=types.InputDocument(
                    id=sandy.media.document.id,
                    access_hash=smex.media.document.access_hash,
                    file_reference=smex.media.document.file_reference,
                ),
                unsave=True,
            )
        )
    except Exception:
        pass

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sspam(?: |$)(.*)" % hl))
async def spam(event: events):
    if event.sender_id in SUDO_USERS:
        jarvis = event.text.split(" ", 2)
        mk = await event.get_reply_message()
        try:
            if len(jarvis) == 3:
                message = jarvis[2]
                for _ in range(int(jarvis[1])):
                    if event.reply_to_msg_id:
                        await mk.reply(message)
                    else:
                        await event.client.send_message(event.chat_id, message)
                    await asyncio.sleep(0.2)
            elif event.reply_to_msg_id and mk.media:
                for _ in range(int(jarvis[1])):
                    mk = await event.client.send_file(event.chat_id, mk, caption=mk.text)
                    await gifspam(event, mk) 
                    await asyncio.sleep(0.2)  
            elif event.reply_to_msg_id and mk.text:
                message = mk.text
                for _ in range(int(jarvis[1])):
                    await event.client.send_message(event.chat_id, message)
                    await asyncio.sleep(0.2)
            else:
                await event.reply(f"😈 **Usage:**\n  » {hl}spam 04 jarvis\n  » {hl}spam 04 <ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ>\n\n**To do spam with replying to a user:**\n  » {hl}spam 04 jarvis <ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ>")
        except (IndexError, ValueError):
            await event.reply(f"😈 **Usage:**\n  » {hl}spam 04 jarvis\n  » {hl}spam 04 <ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ>\n\n**To do spam with replying to a user:**\n  » {hl}spam 04 jarvis <ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ>")
        except Exception as e:
            print(e)

@X1.on(events.NewMessage(incoming=True, pattern=r"\%spspam(?: |$)(.*)" % hl))
async def pspam(event):
    if event.sender_id in SUDO_USERS:
        if event.chat_id in GROUP:
            await event.reply("» YE GROUP JARVIS KE UNDER MAI HAI ISLEYE ISME PSPAM NHI HOGA...")
        else:
            try:
                counter = int(event.text.split(" ", 2)[1])
                porrn = choice(PORMS)
                for _ in range(counter):
                    alt = await event.client.send_file(event.chat_id, porrn)
                    await gifspam(event, alt) 
                    await asyncio.sleep(0.2)
            except (IndexError, ValueError):
                await event.reply(f"🔞 **Usage:**  {hl}pspam 04")
            except Exception as e:
                print(e)

@X1.on(events.NewMessage(incoming=True, pattern=r"\%shang(?: |$)(.*)" % hl))
async def hang(e):
    if e.sender_id in SUDO_USERS:
        if e.chat_id in GROUP:
            await e.reply("» YE GROUP JARVIS KE UNDER MAI HAI ISLEYE ISME HANG NHI HOGA..")
        else:
            try:
                counter = int(e.text.split(" ", 2)[1])
                hang_text = "JARVIS OP 😈꙰꙰꙰꙰꙰꙰⃟꙰⃟꙰⃟꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰꙰⃟꙰⃟꙰⃟꙰"
                await e.respond(hang_text)
                await asyncio.sleep(0.3)
            except (IndexError, ValueError):
                await e.reply(f"😈 **Usage:** {hl}hang 10")
            except Exception as exc:
                print(exc)
