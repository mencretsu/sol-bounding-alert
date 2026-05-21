def format_message(data: dict) -> str:
    name = data["name"]
    symbol = data["symbol"]
    mint = data["mint"]
    similar = data.get("similar_tokens", [])

    msg = f"💊 {name} • ${symbol}\n"
    msg += f"<code>{mint}</code>"

    if similar:
        msg += f"\n\n⚠️ Nama mirip token lama:\n"
        for s in similar[:3]:
            msg += f"┗ {s['name']} • ${s['symbol']}\n"
            msg += f"  <code>{s['mint']}</code>\n"

    return msg
