from datetime import timedelta


def format_berries(amount):
    """
    Format a berry amount with commas and the 🍓 emoji.
    
    Examples:
        format_berries(1000)     -> "1,000 🍓"
        format_berries(-500)     -> "-500 🍓"
        format_berries(1000000)  -> "1,000,000 🍓"
    """
    return f"{amount:,} 🍓"


def format_time_delta(seconds):
    """
    Convert a number of seconds into a human-readable string.
    
    Examples:
        format_time_delta(90)      -> "1m 30s"
        format_time_delta(3661)    -> "1h 1m 1s"
        format_time_delta(45)      -> "45s"
        format_time_delta(86400)   -> "1d 0h 0m"
    """
    if seconds < 0:
        return "0s"
    
    delta = timedelta(seconds=int(seconds))
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0 or days > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{minutes}m")
    if not parts or secs > 0:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def truncate_text(text, max_length=50, suffix="..."):
    """
    Truncate a string to a maximum length, appending a suffix if truncated.
    """
    if not text or len(text) <= max_length:
        return text or ""
    return text[: max_length - len(suffix)].rstrip() + suffix


def get_transaction_emoji(tx_type):
    """
    Return an emoji for a given transaction type.
    """
    emojis = {
        "daily": "⛵",
        "trade": "🤝",
        "raid_win": "⚔️",
        "raid_loss": "💀",
        "purchase": "🛒",
        "reward": "🎁",
    }
    return emojis.get(tx_type, "📌")


def get_transaction_color(tx_type):
    """
    Return a Rich color/style string for a given transaction type.
    """
    colors = {
        "daily": "green",
        "trade": "cyan",
        "raid_win": "bold green",
        "raid_loss": "bold red",
        "purchase": "yellow",
        "reward": "magenta",
    }
    return colors.get(tx_type, "white")