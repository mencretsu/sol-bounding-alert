import httpx
import os

RPC = os.getenv("HELIUS_RPC", "https://api.mainnet-beta.solana.com")

async def get_token_holders(mint: str):
    """Ambil top holders dari token"""
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

async def analyze_token(token_data: dict) -> dict:
    mint = token_data.get("mint", "")
    name = token_data.get("name", "Unknown")
    symbol = token_data.get("symbol", "???")
    market_cap = token_data.get("marketCapSol", 0) * 150  # approx USD
    
    holders = await get_token_holders(mint)
    
    total_supply = sum(float(h["uiAmount"] or 0) for h in holders)
    top_holders = []
    
    for h in holders[:7]:
        amt = float(h["uiAmount"] or 0)
        pct = (amt / total_supply * 100) if total_supply > 0 else 0
        top_holders.append(round(pct, 1))
    
    top10_pct = sum(top_holders[:10])
    
    # Cek bundle sederhana (top holder > 50% = flag)
    dev_holding = top_holders[0] if top_holders else 0
    is_bundled = dev_holding > 50
    bundle_pct = dev_holding if is_bundled else 0

    return {
        "name": name,
        "symbol": symbol,
        "mint": mint,
        "market_cap_usd": market_cap,
        "holder_count": len(holders),
        "top_holders": top_holders,
        "top10_pct": round(top10_pct, 1),
        "dev_holding": dev_holding,
        "is_bundled": is_bundled,
        "bundle_pct": round(bundle_pct, 1),
        "liquidity_sol": token_data.get("vSolInBondingCurve", 0),
        "age_seconds": 1,
    }
