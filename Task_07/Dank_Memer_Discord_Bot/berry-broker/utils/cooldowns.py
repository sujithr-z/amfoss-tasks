from datetime import datetime, timedelta


def check_cooldown(last_action_iso, cooldown_hours=0, cooldown_minutes=0):
    """
    Check if a cooldown period has elapsed since the last action.

    Args:
        last_action_iso (str or None): ISO-formatted timestamp of the last action.
        cooldown_hours (int): Hours to wait.
        cooldown_minutes (int): Minutes to wait.

    Returns:
        dict with:
            - ready (bool): True if cooldown has passed
            - remaining_seconds (int): Seconds left if not ready
            - remaining_text (str): Human-readable time remaining
    """
    if not last_action_iso:
        return {
            "ready": True,
            "remaining_seconds": 0,
            "remaining_text": ""
        }

    try:
        last_action = datetime.fromisoformat(last_action_iso)
    except (ValueError, TypeError):
        return {
            "ready": True,
            "remaining_seconds": 0,
            "remaining_text": ""
        }

    cooldown = timedelta(hours=cooldown_hours, minutes=cooldown_minutes)
    cooldown_end = last_action + cooldown
    now = datetime.now()

    if now >= cooldown_end:
        return {
            "ready": True,
            "remaining_seconds": 0,
            "remaining_text": ""
        }

    remaining = cooldown_end - now
    total_seconds = int(remaining.total_seconds())
    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60
    seconds = remaining.seconds % 60

    if hours > 0:
        text = f"{hours}h {minutes}m"
    elif minutes > 0:
        text = f"{minutes}m {seconds}s"
    else:
        text = f"{seconds}s"

    return {
        "ready": False,
        "remaining_seconds": total_seconds,
        "remaining_text": text
    }


def set_cooldown():
    """
    Return the current timestamp as an ISO string.
    Use this to record when an action was performed.
    """
    return datetime.now().isoformat()