import httpx
import os

RPC = os.getenv("HELIUS_RPC", "https://api.mainnet-beta.solana.com")

async def get_token_info(mint: str) -> dict:
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{mint}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                pairs = data.get("pairs", [])
                if pairs:
                    token = pairs[0].get("baseToken", {})
                    return {
                        "name": token.get("name", "Unknown"),
                        "symbol": token.get("symbol", "???"),
                    }
    except Exception as e:
        print(f"❌ Error fetch token info: {e}")
    return {"name": "Unknown", "symbol": "???"}

async def check_similar_tokens(name: str, mint: str) -> list:
    try:
        words = [w for w in name.split() if len(w) > 2]
        search_term = words[0] if words else name

        url = f"https://api.dexscreener.com/latest/dex/search?q={search_term}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)

            if resp.status_code != 200:
                print(f"⚠️ DexScreener API status: {resp.status_code}")
                return []

            data = resp.json()
            pairs = data.get("pairs", [])

            similar = []
            seen_mints = set()

            for pair in pairs:
                token = pair.get("baseToken", {})
                token_mint = token.get("address", "")
                token_name = token.get("name", "").lower()

                if token_mint == mint or token_mint in seen_mints:
                    continue

                if pair.get("chainId") != "solana":
                    continue

                # Harus beneran mengandung kata yang sama
                if search_term.lower() not in token_name:
                    continue

                seen_mints.add(token_mint)
                similar.append({
                    "name": token.get("name", "Unknown"),
                    "symbol": token.get("symbol", "???"),
                    "mint": token_mint
                })

                if len(similar) >= 3:
                    break

            return similar

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
