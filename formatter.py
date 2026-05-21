def format_message(data: dict) -> str:
    name = data["name"]
    symbol = data["symbol"]
    mint = data["mint"]

    msg = f"""💊 {name} • ${symbol}
<code>{mint}</code>"""
    
    return msg
