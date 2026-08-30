import random
from datetime import datetime, timedelta

from database.connection import get_connection, close_connection
from config import (
    DEFAULT_WALLET,
    DAILY_REWARD_MIN,
    DAILY_REWARD_MAX,
    DAILY_COOLDOWN_HOURS
)


def get_or_create_user(username):
    """Fetch a user from the database, creating one if they don't exist yet."""
    conn = get_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if not user:
            conn.execute(
                "INSERT INTO users (username, wallet) VALUES (?, ?)",
                (username, DEFAULT_WALLET)
            )
            conn.commit()
            user = conn.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()
    finally:
        close_connection(conn)

    return user


def get_user_bounty(username):
    """Return a dict with the user's wallet, bank, and total bounty."""
    user = get_or_create_user(username)
    return {
        "wallet": user["wallet"],
        "bank": user["bank"],
        "total": user["wallet"] + user["bank"]
    }


def claim_daily(username):
    """
    Claim the daily berry reward.
    Returns the reward amount on success.
    Raises ValueError if the cooldown hasn't elapsed.
    """
    user = get_or_create_user(username)

    # Check cooldown
    if user["last_daily"]:
        last_claim = datetime.fromisoformat(user["last_daily"])
        cooldown_end = last_claim + timedelta(hours=DAILY_COOLDOWN_HOURS)
        if datetime.now() < cooldown_end:
            remaining = cooldown_end - datetime.now()
            raise ValueError(
                f"Cooldown active. Try again in {remaining.seconds // 3600}h "
                f"{(remaining.seconds % 3600) // 60}m."
            )

    # Generate reward
    reward = random.randint(DAILY_REWARD_MIN, DAILY_REWARD_MAX)

    conn = get_connection()
    try:
        conn.execute("BEGIN")
        conn.execute(
            "UPDATE users SET wallet = wallet + ?, last_daily = ? WHERE username = ?",
            (reward, datetime.now().isoformat(), username)
        )
        conn.execute(
            """INSERT INTO transactions (user_id, type, amount, description)
               VALUES (?, ?, ?, ?)""",
            (user["id"], "daily", reward, f"Daily reward: plundered {reward} berries")
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        close_connection(conn)

    return reward


def transfer_berries(sender, receiver, amount):
    """
    Transfer berries from one pirate to another.
    Returns a dict with 'success' (bool) and 'message' (str).
    Uses an atomic SQLite transaction to prevent data loss.
    """
    # Validate amount
    if amount <= 0:
        return {"success": False, "message": "Amount must be positive."}

    # Can't trade with yourself
    if sender.lower() == receiver.lower():
        return {"success": False, "message": "You can't trade with yourself."}

    # Ensure both users exist
    sender_user = get_or_create_user(sender)
    receiver_user = get_or_create_user(receiver)

    # Check balance
    if sender_user["wallet"] < amount:
        return {
            "success": False,
            "message": f"Insufficient funds. You only have {sender_user['wallet']:,} berries."
        }

    conn = get_connection()
    try:
        conn.execute("BEGIN")

        # Deduct from sender
        conn.execute(
            "UPDATE users SET wallet = wallet - ? WHERE id = ?",
            (amount, sender_user["id"])
        )

        # Add to receiver
        conn.execute(
            "UPDATE users SET wallet = wallet + ? WHERE id = ?",
            (amount, receiver_user["id"])
        )

        # Record transaction for sender (outgoing)
        conn.execute(
            """INSERT INTO transactions (user_id, type, amount, target_user_id, description)
               VALUES (?, ?, ?, ?, ?)""",
            (sender_user["id"], "trade", -amount, receiver_user["id"],
             f"Sent {amount:,} berries to {receiver}")
        )

        # Record transaction for receiver (incoming)
        conn.execute(
            """INSERT INTO transactions (user_id, type, amount, target_user_id, description)
               VALUES (?, ?, ?, ?, ?)""",
            (receiver_user["id"], "trade", amount, sender_user["id"],
             f"Received {amount:,} berries from {sender}")
        )

        conn.commit()
        return {"success": True, "message": "Trade completed."}

    except Exception as e:
        conn.rollback()
        return {"success": False, "message": f"Transaction failed: {str(e)}"}
    finally:
        close_connection(conn)