from config import X1, SUDO_USERS, CMD_HNDLR as hl
from telethon import events
from telethon.tl.functions.channels import LeaveChannelRequest

async def leave_group(event, group_id):
    try:
        await event.client(LeaveChannelRequest(int(group_id)))
    except Exception as e:
        await event.edit(str(e))

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sleave(?: |$)(.*)" % hl))
async def leave(e):
    if e.sender_id in SUDO_USERS:
        if len(e.text) > 7:
            event = await e.reply("» ʟᴇᴀᴠɪɴɢ ᴛʜᴇ ɢʀᴏᴜᴘ...")
            mkl = e.text.split(" ", 1)
            await leave_group(event, mkl[1])
        else:
            if e.is_private:
                alt = f"**» ʏᴏᴜ ᴄᴀɴ'ᴛ ᴅᴏ ᴛʜɪꜱ ʜᴇʀᴇ**\n\n» {hl}leave <ᴄʜᴀɴɴᴇʟ/ᴄʜᴀᴛ ɪᴅ> \n» {hl}leave : ᴛʏᴘᴇ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ, ʙᴏᴛ ᴡɪʟʟ ᴀᴜᴛᴏ ʟᴇᴀᴠᴇ ᴛʜᴀᴛ ɢʀᴏᴜᴘ."
                await e.reply(alt)
            else:
                event = await e.reply("» ʟᴇᴀᴠɪɴɢ ᴛʜᴇ ɢʀᴏᴜᴘ...")
                await leave_group(event, e.chat_id)
