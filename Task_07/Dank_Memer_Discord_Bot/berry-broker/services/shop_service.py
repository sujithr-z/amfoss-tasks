from database.connection import get_connection, close_connection
from database.queries import (
    get_all_items as db_get_all_items,
    get_item_by_name,
    get_user_inventory as db_get_user_inventory,
)
from services.economy_service import get_or_create_user


def get_all_items():
    """Return all items available in the shop, ordered by price."""
    return db_get_all_items()


def get_user_balance(username):
    """Return the user's wallet and bank balances as a dict."""
    user = get_or_create_user(username)
    return {
        "wallet": user["wallet"],
        "bank": user["bank"],
    }


def get_user_inventory(username):
    """Return the user's inventory items with full item details."""
    user = get_or_create_user(username)
    return db_get_user_inventory(user["id"])


def purchase_item(username, item_name):
    """
    Purchase an item from the shop.
    
    Performs an atomic transaction that:
      1. Deducts the item's price from the user's wallet
      2. Adds the item to the user's inventory (or increments quantity)
      3. Records the transaction in the history log
    
    Returns a dict with:
      - success (bool)
      - message (str)
      - item (dict)        # only on success
      - new_balance (int)  # only on success
    """
    # 1. Look up the item
    item = get_item_by_name(item_name)
    if not item:
        return {
            "success": False,
            "message": f"Item '{item_name}' not found in the shop.",
        }

    # 2. Ensure the user exists and check their balance
    user = get_or_create_user(username)
    price = item["price"]

    if user["wallet"] < price:
        return {
            "success": False,
            "message": (
                f"Insufficient funds. You need {price:,} 🍓 "
                f"but only have {user['wallet']:,} 🍓 in your wallet."
            ),
        }

    # 3. Execute the purchase atomically
    conn = get_connection()
    try:
        conn.execute("BEGIN")

        # Deduct berries
        conn.execute(
            "UPDATE users SET wallet = wallet - ? WHERE id = ?",
            (price, user["id"]),
        )

        # Add to inventory (UPSERT)
        conn.execute(
            """INSERT INTO inventory (user_id, item_id, quantity)
               VALUES (?, ?, 1)
               ON CONFLICT(user_id, item_id)
               DO UPDATE SET quantity = quantity + 1""",
            (user["id"], item["id"]),
        )

        # Record the transaction
        conn.execute(
            """INSERT INTO transactions (user_id, type, amount, description)
               VALUES (?, ?, ?, ?)""",
            (
                user["id"],
                "purchase",
                -price,
                f"Purchased {item['name']} for {price:,} berries",
            ),
        )

        conn.commit()

        # Fetch the updated wallet balance
        updated = conn.execute(
            "SELECT wallet FROM users WHERE id = ?",
            (user["id"],),
        ).fetchone()

        return {
            "success": True,
            "message": f"Purchased {item['name']}!",
            "item": dict(item),
            "new_balance": updated["wallet"],
        }

    except Exception as e:
        conn.rollback()
        return {
            "success": False,
            "message": f"Purchase failed due to an error: {str(e)}",
        }
    finally:
        close_connection(conn)