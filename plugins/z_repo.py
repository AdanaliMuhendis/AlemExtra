import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from AlemMuzik import app
from AlemMuzik.utils.database import add_served_chat, get_assistant


start_txt = """**
✪ HOŞ GELDİN ALEM REPO ✪

➲ ᴇᴀsʏ ʜᴇʀᴏᴋᴜ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ ✰  
➲ ɴᴏ ʙᴀɴ ɪssᴜᴇs ✰  
➲ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅʏɴᴏs ✰  
➲ 𝟸𝟺/𝟽 ʟᴀɢ-ғʀᴇᴇ ✰

► sᴇɴᴅ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ɪғ ʏᴏᴜ ғᴀᴄᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍs!
**"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("Ekle Beni", url=f"https://t.me/{app.username}?startgroup=true")
        ],
        [
          InlineKeyboardButton("HAYATİ", url="https://t.me/AdanaliMuhendis"),
          InlineKeyboardButton("Alem", url="https://t.me/SOHBETALEMİ"),
          ],
               [
                InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/ADANALİMUHENDİS"),

],
[
              InlineKeyboardButton("ᴍᴜsɪᴄ", url=f"https://github.com/AdanaliMuhendis/AlemMuzik"),
              InlineKeyboardButton("-", url=f"-"),
              ],
              [
              InlineKeyboardButton("ᴍᴀɴᴀɢᴍᴇɴᴛ", url=f"-"),
InlineKeyboardButton("ᴄʜᴀᴛʙᴏᴛ", url=f"-"),
]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo=config.START_IMG_URL,
        caption=start_txt,
        reply_markup=reply_markup
    )




@app.on_message(
    filters.command(
        ["hi", "hii", "hello", "hui", "good", "gm", "ok", "bye", "welcome", "thanks"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & filters.group
)
async def bot_check(_, message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)

