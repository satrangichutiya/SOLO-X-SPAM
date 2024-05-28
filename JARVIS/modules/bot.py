import sys
import heroku3
from os import execl, getenv
from datetime import datetime
from telethon import events, Button
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantsAdmins
from config import X1, OWNER_ID, SUDO_USERS, HEROKU_APP_NAME, HEROKU_API_KEY, CMD_HNDLR as hl

REQUIRED_CHANNELS = ["JARVIS_V_SUPPORT", "Dora_Hub"]  # Replace with actual group/channel usernames or IDs

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sping(?: |$)(.*)" % hl))
async def ping(e):
    if e.sender_id in SUDO_USERS:
        start = datetime.now()
        jarvis = await e.reply(f"❄️")
        end = datetime.now()
        mp = (end - start).microseconds / 1000
        await jarvis.edit(f"[𝐉𝐀𝐑𝐕𝐈𝐒 𝐈𝐒 𝐑𝐄𝐀𝐃𝐘 𝐓𝐎  ](https://t.me/JARVIS_V_SUPPORT)[𝐅𝐔𝐂𝐊 𝐇𝐀𝐓𝐄𝐑𝐒 🥀](https://t.me/Dora_Hub)🤖\n» `{mp} ᴍꜱ`")
    else:
        await prompt_join_channels(e)

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sreboot(?: |$)(.*)" % hl))
async def restart(e):
    if e.sender_id in SUDO_USERS:
        await e.reply(f"`BOT IS RESTARTING PLEASE WAIT.`")
        try:
            await X1.disconnect()
        except Exception:
            pass
        execl(sys.executable, sys.executable, *sys.argv)
    else:
        await prompt_join_channels(e)

@X1.on(events.NewMessage(incoming=True, pattern=r"\%ssudo(?: |$)(.*)" % hl))
async def addsudo(event):
    if event.sender_id == OWNER_ID:
        await manage_sudo_users(event, add=True)
    elif event.sender_id in SUDO_USERS:
        await event.reply("» BSDK SIRF JARVIS SUDO DE SKTA HAI...")
    else:
        await prompt_join_channels(event)

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sremovesudo(?: |$)(.*)" % hl))
async def removesudo(event):
    if event.sender_id == OWNER_ID:
        await manage_sudo_users(event, add=False)
    else:
        await event.reply("Only Jarvis can remove sudo users.")

@X1.on(events.NewMessage(incoming=True, pattern=r"\%ssudos(?: |$)(.*)" % hl))
async def show_sudo_users(event):
    if event.sender_id == OWNER_ID:
        sudo_users_list = "Jarvis Ke Bache hai ye:\n"
        for user_id in SUDO_USERS:
            sudo_users_list += f"- {user_id}\n"
        await event.reply(sudo_users_list)
    else:
        await event.reply("Only Jarvis can view the sudo users list.")

@X1.on(events.NewMessage(incoming=True, pattern=r"\%saddmultisudo(?: |$)(.*)" % hl))
async def addmultisudo(event):
    if event.sender_id == OWNER_ID:
        await manage_multiple_sudo_users(event)
    elif event.sender_id in SUDO_USERS:
        await event.reply("Only Jarvis can add sudo users.")
    else:
        await prompt_join_channels(event)

@X1.on(events.NewMessage(incoming=True, pattern=r"\%sgetsudo(?: |$)(.*)" % hl))
async def getsudo(event):
    if event.sender_id not in SUDO_USERS:
        for channel in REQUIRED_CHANNELS:
            try:
                participants = await X1(GetParticipantsRequest(
                    channel=channel,
                    filter=ChannelParticipantsSearch(''),
                    offset=0,
                    limit=100,
                    hash=0
                ))
                if not any(participant.id == event.sender_id for participant in participants.users):
                    await prompt_join_channels(event)
                    return
            except Exception as ex:
                await event.reply(f"Error checking membership for {channel}: {ex}")
                return
        await manage_sudo_users(event, add=True)
    else:
        await event.reply("You already have sudo privileges.")

async def manage_sudo_users(event, add):
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    sudousers = getenv("SUDO_USERS", default=None)
    if add:
        ok = await event.reply(f"» __Jarvis Ka Ek Beta Aur Add Ho rha hai..__")
    else:
        ok = await event.reply("YE Jarvis Ki Najayaz Aulad thi isiliye nikal diya💋...")
    target = event.sender_id
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await ok.edit("`[HEROKU]:" "\nPlease Setup Your` **HEROKU_APP_NAME**")
        return
    heroku_var = app.config()
    if add:
        if str(target) in sudousers:
            await ok.edit(f"YE BHI JARVIS KA HI BACHA HAI.. !!")
        else:
            newsudo = f"{sudousers} {target}" if sudousers else f"{target}"
            await ok.edit(f"» **ɴᴇᴡ ꜱᴜᴅᴏ ᴜꜱᴇʀ**: `{target}`\n» `ADD KAR DIYE HAI SUDO..BOT RESTART HO RHA HAI`")
            heroku_var["SUDO_USERS"] = newsudo
    else:
        if str(target) not in sudousers:
            await ok.edit("User is not in the sudo list.")
        else:
            new_sudo_users = " ".join([user for user in sudousers.split() if user != str(target)])
            await ok.edit(f"Removed sudo user: `{target}`")
            heroku_var["SUDO_USERS"] = new_sudo_users

async def manage_multiple_sudo_users(event):
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    sudousers = getenv("SUDO_USERS", default=None)
    ok = await event.reply(f"Adding new sudo users...")
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await ok.edit("`[HEROKU]:" "\nPlease Setup Your` **HEROKU_APP_NAME**")
        return
    heroku_var = app.config()
    new_sudo_users = sudousers.split() if sudousers else []
    try:
        target_ids = [int(x) for x in event.pattern_match.group(1).split()]
    except:
        await ok.edit("Error processing the user IDs.")
        return
    target_ids = list(set(target_ids))
    new_sudo_users.extend(str(user_id) for user_id in target_ids if str(user_id) not in new_sudo_users)
    new_sudo_users_str = ' '.join(new_sudo_users)
    heroku_var["SUDO_USERS"] = new_sudo_users_str
    await ok.edit(f"Added {len(target_ids)} new sudo users.")

async def prompt_join_channels(event):
    buttons = [
        [Button.url("Join JARVIS V SUPPORT", "https://t.me/JARVIS_V_SUPPORT")],
        [Button.url("Join Dora Hub", "https://t.me/Dora_Hub")]
    ]
    await event.reply("To use this feature, please join the following channels:", buttons=buttons)
