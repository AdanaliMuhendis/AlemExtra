import logging
import os
from pyrogram import filters
from pyrogram.types import Message
from TheAPI import api
from AlemMuzik import app

# Setup logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

@app.on_message(filters.command(["tgm"]))
async def get_link_group(client, message):
    user = message.from_user
    logging.info(f"Received media from {user.first_name}")

    # Check if the message is a reply to a media message
    if not message.reply_to_message:
        await message.reply_text("Please reply to a media message.")
        return

    media = message.reply_to_message
    file_size = 0
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size

    if file_size > 15 * 1024 * 1024:
        await message.reply_text("Please provide a media file under 15MB.")
        return

    try:
        text = await message.reply_text("Processing...")

        async def progress(current, total):
            try:
                await text.edit_text(f"Downloading... {current * 100 / total:.1f}%")
            except Exception:
                pass

        try:
            local_path = await media.download(progress=progress)
            await text.edit_text("Uploading to Telegraph...")

            upload_result = api.upload_image(local_path)

            if isinstance(upload_result, str):
                await text.edit_text(f"Here is your link: {upload_result}")
            else:
                await text.edit_text(f"Failed to upload the media. Please try again later.\n\nReason: {upload_result}")

            try:
                os.remove(local_path)
            except Exception:
                pass

        except Exception as e:
            await text.edit_text(f"Failed to upload the media. Please try again later.\n\nReason: {e}")
            try:
                os.remove(local_path)
            except Exception:
                pass
            return
    except Exception:
        pass