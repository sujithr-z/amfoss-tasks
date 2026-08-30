import sqlite3
from database.connection import get_connection, close_connection
from data.shop_items import get_seed_items

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            wallet INTEGER DEFAULT 1000,
            bank INTEGER DEFAULT 0,
            last_daily TEXT,
            last_raid TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price INTEGER NOT NULL,
            description TEXT,
            effect TEXT
        );
        
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            active INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
            UNIQUE(user_id, item_id)
        );
        
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount INTEGER NOT NULL,
            target_user_id INTEGER,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    
    # Handle schema migration if users table existed without last_raid
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN last_raid TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    seed_items = get_seed_items()
    for item in seed_items:
        try:
            cursor.execute(
                "INSERT INTO items (name, price, description, effect) VALUES (?, ?, ?, ?)",
                item
            )
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    close_connection(conn)