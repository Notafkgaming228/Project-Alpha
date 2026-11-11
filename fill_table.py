import sqlite3
import os
from datetime import datetime
if os.path.isdir("data"):
    pass
else:
    os.mkdir("data")
now = datetime.now()
if not os.path.isdir("data/tasks.db"):
    connection = sqlite3.connect("data/tasks.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        level INTEGER CHECK (level >= 1 AND level <= 3) NOT NULL
    )
    """)
    connection.commit()
    connection.close()
conn = sqlite3.connect("data/tasks.db")
now = datetime.now()
date = now.strftime("%Y-%m-%d")
time = now.strftime("%H:%M")
conn.executemany(
    "INSERT INTO tasks (date, time, name, description, level) VALUES (?, ?, ?, ?, ?)",
    [
        (date, time, "Низкий приоритет",  "Описание 1", 1),
        (date, time, "Средний приоритет", "Описание 2", 2),
        (date, time, "Высокий приоритет", "Описание 3", 3),
    ]
)
conn.commit()
conn.close()
print("Done")