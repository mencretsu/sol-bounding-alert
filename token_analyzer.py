import httpx
import os

RPC = os.getenv("HELIUS_RPC", "https://api.mainnet-beta.solana.com")

async def get_token_holders(mint: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(RPC, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenLargestAccounts",
            "params": [mint]
        })
        data = resp.json()
        accounts = data.get("result", {}).get("value", [])
        return accounts

async def check_similar_tokens(name: str, mint: str) -> list:
    try:
        url = f"https://frontend-api.pump.fun/coins?searchTerm={name}&limit=10"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Origin": "https://pump.fun",
            "Referer": "https://pump.fun/"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, timeout=10)
            
            if resp.status_code != 200:
                print(f"⚠️ Similar tokens API status: {resp.status_code}")
                return []
            
            coins = resp.json()
            
            similar = []
            for coin in coins:
                if coin["mint"] == mint:
                    continue
                similar.append({
                    "name": coin["name"],
                    "symbol": coin["symbol"],
                    "mint": coin["mint"]
                })
            
            return similar
    except Exception as e:
        print(f"❌ Error cek similar tokens: {e}")
        return []

async def analyze_token(token_data: dict) -> dict:
    mint = token_data.get("mint", "")
    name = token_data.get("name", "Unknown")
    symbol = token_data.get("symbol", "???")

    similar = await check_similar_tokens(name, mint)

    return {
        "name": name,
        "symbol": symbol,
        "mint": mint,
        "similar_tokens": similar,
    }
