from pyrogram import Client, filters, enums
from os import environ

app_id = int(environ.get('API_ID'))
api_hash = environ.get('API_HASH')
bot_token = environ.get('BOT_TOKEN')
to_chat_id = int(environ.get('TO_CHAT'))
from_chat_id = int(environ.get('FROM_CHAT'))

webxzonebot = Client(    
    name='webxzonebot',
    api_id=app_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@webxzonebot.on_message(filters.chat(from_chat_id))
async def forward_media(_, message):
    try:
        if message.chat.id == to_chat_id:
            return

        caption = message.caption or ""

        if message.video:
            media = message.video.file_id
            media_type = "video"
        elif message.document:
            media = message.document.file_id
            media_type = "document"
        else:
            return

        await _.send_cached_media(
            chat_id=to_chat_id,
            file_id=media,
            caption=f"**{caption}**" if caption else None,
            parse_mode=enums.ParseMode.MARKDOWN
        )

        print(f"✅ Forwarded {media_type} from {message.chat.id} → {to_chat_id}")

    except Exception as e:
        print(f"⚠️ Error while forwarding: {e}")
        

@webxzonebot.on_message(filters.command('start') & filters.user(5163706369))
async def start(bot, message):
    await message.reply('Alive')

print('Bot Started!')
webxzonebot.run()
