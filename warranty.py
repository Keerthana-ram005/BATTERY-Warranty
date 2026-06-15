# import sqlite3

# def create_connection():
#     return sqlite3.connect("warranty.db")

# def create_tables():
#     conn = create_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS (
#         user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_name TEXT NOT NULL,
#         password TEXT NOT NULL,
#         role TEXT NOT NULL
#     )
#     """)

#     conn.commit()
#     conn.close()