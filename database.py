import sqlite3

def get_db():
    conn = sqlite3.connect("sales.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Type (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Item (
            id INTEGER PRIMARY KEY,
            name TEXT,
            priceUSD INTEGER,
            type_id INTEGER,
            FOREIGN KEY (type_id) REFERENCES Type(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            password TEXT
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS UserLikedItems (
        user_id INTEGER,
        item_id INTEGER,
        PRIMARY KEY (user_id, item_id),
        FOREIGN KEY (user_id) REFERENCES User(id),
        FOREIGN KEY (item_id) REFERENCES Item(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()