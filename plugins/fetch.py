from pyrogram import Client, filters
import re
from ChampuMusic import app
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid
from pyrogram.enums import MessageMediaType
import os

async def link_checker(userbot, message):
    pattern = r'https?://\S+'
    match = re.search(pattern, message.text)
    if match:
        extracted_link = match.group(0)
        msg_id = extracted_link.split("/")[-1]
        if extracted_link.split("/")[-3] == "c":
            chat_id = int("-100" + extracted_link.split("/")[-2])
            return chat_id, int(msg_id), "private"
        elif msg_id.startswith("+"):
            # Assuming the bot can join the chat if it's a private link
            xx = await userbot.join_chat(extracted_link)
            return True, xx, None
        else:
            chat_id = extracted_link.split("/")[-2]
            return chat_id, int(msg_id), "public"
    return None, None, None

async def progress_bar(current, total):
    percentage = (current / total) * 100
    print(f"Download progress: {percentage:.2f}%")

@app.on_message(filters.command("fetch") & filters.private)
async def fetch_message(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage:**\n`/fetch <message_link>`")
        return

    message_link = message.command[1]

    # Use link_checker to get chat_id and message_id
    chat_id, message_id, chat_type = await link_checker(client, message)

    if chat_id is None or message_id is None:
        await message.reply_text("**Invalid message link.")
        return

    try:
        # Fetch the message from the specified chat
        fetched_message = await client.get_messages(chat_id, message_id)

        # Log the fetched message for debugging
        print(f"Fetched message: {fetched_message}")

        # Check for service messages
        if fetched_message.service:
            await message.reply_text("This message is a service message.")
            return

        # Handle media
        if fetched_message.media:
            # Download media with progress
            file = await client.download_media(fetched_message, progress=progress_bar)
            if fetched_message.media == MessageMediaType.VIDEO:
                await client.send_video(message.chat.id, file, caption=fetched_message.caption)
            elif fetched_message.media == MessageMediaType.PHOTO:
                await client.send_photo(message.chat.id, file, caption=fetched_message.caption)
            elif fetched_message.media == MessageMediaType.AUDIO:
                await client.send_audio(message.chat.id, file, caption=fetched_message.caption)
            elif fetched_message.media == MessageMediaType.DOCUMENT:
                await client.send_document(message.chat.id, file, caption=fetched_message.caption)
            elif fetched_message.media == MessageMediaType.VOICE:
                await client.send_voice(message.chat.id, file, caption=fetched_message.caption)
            elif fetched_message.media == MessageMediaType.STICKER:
                await client.send_sticker(message.chat.id, file)
            elif fetched_message.media == MessageMediaType.GIF:
                await client.send_animation(message.chat.id, file, caption=fetched_message.caption)
            else:
                await client.send_document(message.chat.id, file, caption=fetched_message.caption)

        else:
            # Handle text messages
            response_text = fetched_message.text if fetched_message.text else "This message does not contain text."
            await message.reply_text(response_text)

        # Include additional information about the message type
        chat_type = fetched_message.chat.type if fetched_message.chat else "Unknown"
        from_user = fetched_message.from_user.first_name if fetched_message.from_user else 'Unknown'
        response_text += f"\n\n**Message Type: {chat_type}\n" \
                         f"**From: {from_user}"

        await message.reply_text(f"Fetched Message:\n{response_text}")

    except Exception as e:
        if isinstance(e, (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid)):
            await message.reply_text("Error: The bot does not have permission to access this chat or message.")
        else:
            await message.reply_text(f"Error: {str(e)}")