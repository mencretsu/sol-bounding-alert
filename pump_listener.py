import asyncio
import json
import websockets

PUMP_WS = "wss://pumpportal.fun/api/data"

async def listen_new_tokens(callback):
    while True:
        try:
            async with websockets.connect(PUMP_WS) as ws:
                # Subscribe ke event token baru yang bonding subscribeNewToken, subscribeMigration
                payload = {
                    "method": "subscribeNewToken"
                }
                await ws.send(json.dumps(payload))
                print("✅ Connected to PumpFun WebSocket")

                async for message in ws:
                    data = json.loads(message)
                    if data.get("txType") == "create":
                        await callback(data)
        except Exception as e:
            print(f"WS Error: {e}, reconnecting in 5s...")
            await asyncio.sleep(5)
