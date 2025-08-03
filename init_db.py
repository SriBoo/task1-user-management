import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.executemany('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', [
        ('John Doe', 'john@example.com', 'password123'),
        ('Jane Smith', 'jane@example.com', 'secret456'),
        ('Bob Johnson', 'bob@example.com', 'qwerty789'),
    ])
    conn.commit()
    conn.close()
    print("Database initialized with sample data")

if __name__ == '__main__':
    init_db()
