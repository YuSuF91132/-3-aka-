import sqlite3

conn = sqlite3.connect('delivery_bot.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product TEXT,
            address TEXT,
            phone TEXT
        )
    ''')
    conn.commit()

def add_order(user_id, product, address, phone):
    cursor.execute("INSERT INTO orders (user_id, product, address, phone) VALUES (?, ?, ?, ?)", (user_id, product, address, phone))
    conn.commit()

def get_all_orders():
    cursor.execute("SELECT * FROM orders")
    return cursor.fetchall()