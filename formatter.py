def format_message(data: dict) -> str:
    name = data["name"]
    symbol = data["symbol"]
    mint = data["mint"]
    mc = data["market_cap_usd"]
    liq_sol = data["liquidity_sol"]
    liq_usd = liq_sol * 150
    holders = data["holder_count"]
    top_holders = data["top_holders"]
    top10 = data["top10_pct"]
    dev = data["dev_holding"]
    bundled = data["bundle_pct"]
    is_bundled = data["is_bundled"]

    # Flags
    bundle_flag = f"🚨 High Holder | Dev Bundled {bundled}%" if is_bundled else ""
    high_top10 = "⚠️ High Top Ten" if top10 > 60 else ""
    alert_line = "🔴 Alert" if is_bundled or top10 > 60 else "🟢 OK"

    holders_str = " | ".join([f"{h}%" for h in top_holders[:7]])

    msg = f"""💊🔁 {name} • ${symbol}
{mint}
"""
    if bundle_flag:
        msg += f"{bundle_flag}\n"
    if high_top10:
        msg += f"{high_top10}\n"
    
    msg += f"""➕ Mint: 🤍 | 🧊 Freeze: 🤍
{alert_line}
🕒 Age: 1s [0%] 💰 MC: ${mc:,.0f}
💧 Liq: ${liq_usd:,.1f}K [{liq_sol:.0f} SOL]
┗ Fake: $0
🦅 Dex: Paid❌ Ads❌
👥 Hodls: {holders} • Top: {top10}% {"⚠️" if top10 > 60 else ""}
┗ High: {holders_str}
📦 /Bundles: 1 • {bundled}% → 0%
🛠️ Dev: 0 SOL • {dev}%
┗ Bundled: {bundled}% {"🚨" if is_bundled else "🟢"} | Sold: 0% 🟢
"""
    return msg
