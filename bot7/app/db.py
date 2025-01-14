import sqlite3

def init_db():
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()



def save_to_db(user_id: int, time: str):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO schedules (user_id, time) VALUES (?, ?)", (user_id, time))
    conn.commit()
    conn.close()


def get_user_schedule(user_id: int):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM schedules WHERE user_id = ?", (user_id,))
    result = cursor.fetchall()
    conn.close()
    return [row[0] for row in result]


def delete_schedule(user_id: int, time: str):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM schedules WHERE user_id = ? AND time = ?", (user_id, time))
    conn.commit()
    conn.close()



