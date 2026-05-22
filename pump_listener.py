import asyncio
import json
import websockets

PUMP_WS = "wss://pumpportal.fun/api/data"

async def listen_new_tokens(callback):
    while True:
        try:
            async with websockets.connect(
                PUMP_WS,
                ping_interval=20,
                ping_timeout=10
            ) as ws:
                payload = {"method": "subscribeMigration"}
                await ws.send(json.dumps(payload))
                print("✅ Connected to PumpFun WebSocket")

                async for message in ws:
                    data = json.loads(message)
                    
                    # Skip pesan konfirmasi
                    if "message" in data:
                        print(f"ℹ️ Info: {data['message']}")
                        continue
                    
                    await callback(data)

        except Exception as e:
            print(f"WS Error: {e}, reconnecting in 5s...")
            await asyncio.sleep(5)
