import asyncio
import os
from dotenv import load_dotenv

from pump_listener import listen_new_tokens
from token_analyzer import analyze_token
from formatter import format_message
from telegram_bot import init_bot, send_token_alert

load_dotenv()
init_bot()

async def handle_new_token(token_data: dict):
    try:
        print(f"New token: {token_data.get('name')} - {token_data.get('mint')}")
        analyzed = await analyze_token(token_data)
        msg = format_message(analyzed)
        await send_token_alert(msg)
        print("✅ Sent to Telegram")
    except Exception as e:
        print(f"Error handling token: {e}")

async def main():
    print("🚀 Starting PumpFun Bot...")
    await listen_new_tokens(handle_new_token)

if __name__ == "__main__":
    asyncio.run(main())
