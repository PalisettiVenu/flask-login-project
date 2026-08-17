import sqlite3


def get_db_connection():
    conn = sqlite3.connect("database.db")
    return conn


def create_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    """)

    conn.commit()
    conn.close()