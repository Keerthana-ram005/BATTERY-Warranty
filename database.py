import sqlite3 
conn=sqlite3.connect("warranty.db")
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
               user_id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_name TEXT NOT NULL,
               password TEXT NOT NULL,
               role TEXT NOT NULL)
               """)
conn.commit()
conn.close()