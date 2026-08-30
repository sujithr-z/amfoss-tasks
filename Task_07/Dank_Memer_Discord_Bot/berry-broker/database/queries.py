import sqlite3
from database.connection import get_connection, close_connection

def get_user(username):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    close_connection(conn)
    return user

def create_user(username):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    except sqlite3.IntegrityError:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    close_connection(conn)
    return user

def update_wallet(username, amount):
    conn = get_connection()
    conn.execute("UPDATE users SET wallet = wallet + ? WHERE username = ?", (amount, username))
    conn.commit()
    close_connection(conn)

def get_all_items():
    conn = get_connection()
    items = conn.execute("SELECT * FROM items ORDER BY price ASC").fetchall()
    close_connection(conn)
    return items

def get_item_by_name(name):
    conn = get_connection()
    item = conn.execute("SELECT * FROM items WHERE LOWER(name) = LOWER(?)", (name.strip(),)).fetchone()
    close_connection(conn)
    return item

def add_to_inventory(user_id, item_id, quantity=1):
    conn = get_connection()
    conn.execute(
        """INSERT INTO inventory (user_id, item_id, quantity) 
           VALUES (?, ?, ?) 
           ON CONFLICT(user_id, item_id) 
           DO UPDATE SET quantity = quantity + ?""",
        (user_id, item_id, quantity, quantity)
    )
    conn.commit()
    close_connection(conn)

def get_user_inventory(user_id):
    conn = get_connection()
    items = conn.execute(
        """SELECT i.name, i.price, i.description, i.effect, inv.quantity, inv.active
           FROM inventory inv
           JOIN items i ON inv.item_id = i.id
           WHERE inv.user_id = ?
           ORDER BY i.name ASC""",
        (user_id,)
    ).fetchall()
    close_connection(conn)
    return items

def has_item(user_id, item_name):
    conn = get_connection()
    result = conn.execute(
        """SELECT inv.quantity FROM inventory inv
           JOIN items i ON inv.item_id = i.id
           WHERE inv.user_id = ? AND LOWER(i.name) = LOWER(?)""",
        (user_id, item_name.strip())
    ).fetchone()
    close_connection(conn)
    return result is not None and result["quantity"] > 0

def record_transaction(user_id, tx_type, amount, target_user_id=None, description=""):
    conn = get_connection()
    conn.execute(
        """INSERT INTO transactions (user_id, type, amount, target_user_id, description) 
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, tx_type, amount, target_user_id, description)
    )
    conn.commit()
    close_connection(conn)

def get_transaction_history(user_id, limit=20):
    conn = get_connection()
    history = conn.execute(
        """SELECT t.*, u.username as target_username
           FROM transactions t
           LEFT JOIN users u ON t.target_user_id = u.id
           WHERE t.user_id = ?
           ORDER BY t.timestamp DESC
           LIMIT ?""",
        (user_id, limit)
    ).fetchall()
    close_connection(conn)
    return history

def get_leaderboard(limit=10):
    conn = get_connection()
    leaders = conn.execute(
        """SELECT username, wallet, bank, (wallet + bank) as total_wealth
           FROM users
           ORDER BY total_wealth DESC
           LIMIT ?""",
        (limit,)
    ).fetchall()
    close_connection(conn)
    return leaders

def transfer_berries(sender, receiver, amount):
    conn = get_connection()
    try:
        conn.execute("BEGIN")
        conn.execute("UPDATE users SET wallet = wallet - ? WHERE username = ?", (amount, sender))
        conn.execute("UPDATE users SET wallet = wallet + ? WHERE username = ?", (amount, receiver))
        sender_row = conn.execute("SELECT id FROM users WHERE username = ?", (sender,)).fetchone()
        receiver_row = conn.execute("SELECT id FROM users WHERE username = ?", (receiver,)).fetchone()
        conn.execute(
            "INSERT INTO transactions (user_id, type, amount, target_user_id, description) VALUES (?, ?, ?, ?, ?)",
            (sender_row["id"], "trade", -amount, receiver_row["id"], f"Sent {amount:,} berries to {receiver}")
        )
        conn.execute(
            "INSERT INTO transactions (user_id, type, amount, target_user_id, description) VALUES (?, ?, ?, ?, ?)",
            (receiver_row["id"], "trade", amount, sender_row["id"], f"Received {amount:,} berries from {sender}")
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        close_connection(conn)