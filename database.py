import sqlite3

def get_db():
    conn = sqlite3.connect("sales.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS City (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            filepath TEXT,
            item_id INTEGER,
            FOREIGN KEY (item_id) REFERENCES Item(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            password TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            priceUSD INTEGER,
            type_id INTEGER,
            description TEXT,
            phone TEXT,
            city_id INTEGER,
            FOREIGN KEY (type_id) REFERENCES Type(id),
            FOREIGN KEY (city_id) REFERENCES City(id),
            FOREIGN KEY (user_id) REFERENCES User(id)
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Comment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_id INTEGER,
        text TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()