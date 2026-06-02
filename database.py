import sqlite3

def create_connection():
    return sqlite3.connect("warranty.db")

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def add_user(username, password, role):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(user_name, password, role) VALUES (?, ?, ?)",
        (username, password, role)
    )

    conn.commit()
    conn.close()

def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_name=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user