# PumpFun Migration Alert Bot

Telegram bot that monitors PumpFun token migrations to Raydium and sends real-time alerts.

## Setup

1. Clone this repo
2. Set environment variables in Railway:
   - `TELEGRAM_BOT_TOKEN` — from [@BotFather](https://t.me/BotFather)
   - `TELEGRAM_CHANNEL_ID` — your channel (e.g. `@mychannel`)
   - `HELIUS_RPC` — from [helius.dev](https://helius.dev)
3. Deploy to [Railway](https://railway.app)

## Stack

- PumpFun WebSocket — migration events
- DexScreener API — token info & similar token search
- Telegram Bot — notifications

## Output Example

```
💊 Trump Squad • $TRUMPSQUAD
CR7omZeRdSiEUiR6d1DDt6uQjhBZYQ9ouyR5GEzepump

⚠️ Similar old tokens found:
┗ Trump • $TRUMP
  6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN
```
