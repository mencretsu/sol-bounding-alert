import asyncio
import time
from dotenv import load_dotenv

from pump_listener import listen_new_tokens
from token_analyzer import analyze_token
from formatter import format_message
from telegram_bot import init_bot, send_token_alert

load_dotenv()
init_bot()

MAX_AGE_SECONDS = 60
sent_mints = set()

async def handle_new_token(token_data: dict):
    try:
        mint = token_data.get("mint", "")

        # Skip duplikat
        if mint in sent_mints:
            print(f"⏭️ Skip duplikat: {mint}")
            return

        # Cek umur token
        token_time = token_data.get("timestamp", time.time() * 1000) / 1000
        age = time.time() - token_time

        if age > MAX_AGE_SECONDS:
            print(f"⏭️ Skip, token udah {int(age)}s")
            return

        # Bersihin cache kalau udah gede banget
        if len(sent_mints) > 10000:
            sent_mints.clear()
            print("🧹 Cache dibersihkan")

        sent_mints.add(mint)

        print(f"🆕 New token: {token_data.get('name')} - umur {int(age)}s")
        analyzed = await analyze_token(token_data)
        msg = format_message(analyzed)
        await send_token_alert(msg)
        print("✅ Sent to Telegram")

    except Exception as e:
        print(f"❌ Error handling token: {e}")

async def main():
    print("🚀 Starting PumpFun Bot...")
    await listen_new_tokens(handle_new_token)

if __name__ == "__main__":
    asyncio.run(main())
