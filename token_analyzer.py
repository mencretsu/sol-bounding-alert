import httpx
import os

RPC = os.getenv("HELIUS_RPC", "https://api.mainnet-beta.solana.com")

async def get_token_info(mint: str) -> dict:
    try:
        url = f"https://frontend-api.pump.fun/coins/{mint}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Origin": "https://pump.fun",
            "Referer": "https://pump.fun/"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, timeout=10)
            print(f"🔍 Token info status: {resp.status_code}")  # tambahin ini
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "name": data.get("name", "Unknown"),
                    "symbol": data.get("symbol", "???"),
                }
    except Exception as e:
        print(f"❌ Error fetch token info: {e}")
    return {"name": "Unknown", "symbol": "???"}

async def check_similar_tokens(name: str, mint: str) -> list:
    try:
        words = [w for w in name.split() if len(w) > 2]
        search_term = words[0] if words else name

        url = f"https://frontend-api.pump.fun/coins?searchTerm={search_term}&limit=10"
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

            return similar[:3]

    except Exception as e:
        print(f"❌ Error cek similar tokens: {e}")
        return []

async def analyze_token(token_data: dict) -> dict:
    mint = token_data.get("mint", "")

    info = await get_token_info(mint)
    name = info["name"]
    symbol = info["symbol"]

    similar = await check_similar_tokens(name, mint)

    return {
        "name": name,
        "symbol": symbol,
        "mint": mint,
        "similar_tokens": similar,
    }
