import logging
from pyrogram import Client, filters, enums
from os import environ

app_id = int(environ.get("API_ID"))
api_hash = environ.get("API_HASH")
bot_token = environ.get("BOT_TOKEN")

to_chat_id = int(environ.get("TO_CHAT"))
from_chat_id = int(environ.get("FROM_CHAT"))


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ForwardBot")

webxzonebot = Client(
    name="webxzonebot",
    api_id=app_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@webxzonebot.on_message(filters.chat(from_chat_id) & (filters.video | filters.document))
async def forward_media(client, message):
    try:
        if message.chat.id == to_chat_id:
            return

        caption = message.caption or ""
        media_type = "video" if message.video else "document"
        media = message.video.file_id if message.video else message.document.file_id

        await client.send_cached_media(
            chat_id=to_chat_id,
            file_id=media,
            caption=f"**{caption}**" if caption else None,
            parse_mode=enums.ParseMode.MARKDOWN
        )

        logger.info(f"✅ Forwarded {media_type} from {message.chat.id} → {to_chat_id}")

    except Exception as e:
        logger.exception(f"⚠️ Error while forwarding message: {e}")


@webxzonebot.on_message(filters.command("start") & filters.user(5163706369))
async def start(_, message):
    await message.reply_text("✅ Bot is Alive!")
    logger.info(f"Start command used by {message.from_user.id}")

if __name__ == "__main__":
    logger.info("🚀 Bot Started and Listening for media...")
    webxzonebot.run()
