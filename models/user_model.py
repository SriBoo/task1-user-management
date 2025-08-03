import sqlite3

DB_NAME = 'users.db'

def get_all_users():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
    return [{"id": row[0], "name": row[1], "email": row[2], "password": row[3]} for row in rows]

def get_user_by_id(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
    if row:
        return {"id": row[0], "name": row[1], "email": row[2], "password": row[3]}
    return None

def add_user(name, email, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                       (name, email, password))
        conn.commit()
        return cursor.lastrowid
