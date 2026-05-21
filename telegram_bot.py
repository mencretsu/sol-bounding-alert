import os
from telegram import Bot

bot = None

def init_bot():
    global bot
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

async def send_token_alert(message: str):
    channel = os.getenv("TELEGRAM_CHANNEL_ID")
    await bot.send_message(
        chat_id=channel,
        text=message,
        parse_mode="HTML"
    )
