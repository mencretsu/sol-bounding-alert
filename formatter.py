def format_message(data: dict) -> str:
    name = data["name"]
    symbol = data["symbol"]
    mint = data["mint"]
    similar_names = data.get("similar_names", [])
    similar_ticks = data.get("similar_ticks", [])

    msg = f"💊 {name} • ${symbol}\n"
    msg += f"<code>{mint}</code>"

    if similar_names:
        msg += f"\n\n⚠️ Found {len(similar_names)} similar name ({name})"
        for s in similar_names:
            msg += f"\n┗ ${s['symbol']} • <code>{s['mint']}</code>"

    if similar_ticks:
        msg += f"\n\n⚠️ Found {len(similar_ticks)} similar tick (${symbol})"
        for s in similar_ticks:
            msg += f"\n┗ ${s['symbol']} • <code>{s['mint']}</code>"

    return msg
