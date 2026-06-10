import sqlite3
from datetime import datetime

DB_NAME = 'guestbook.db'

def get_db_connection():
    """Создаёт соединение с базой данных"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализирует базу данных: создаёт таблицу messages, если её нет"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all_messages():
    """Возвращает все сообщения, отсортированные по дате (от новых к старым)"""
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY created_at DESC').fetchall()
    conn.close()
    return messages

def add_message(name, message):
    """Добавляет новое сообщение в базу данных"""
    conn = get_db_connection()
    created_at = datetime.now().isoformat()
    conn.execute(
        'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
        (name, message, created_at)
    )
    conn.commit()
    conn.close()

def delete_message(message_id):
    """Удаляет сообщение из базы данных по его id"""
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()

def get_message_count():
    """Возвращает общее количество сообщений"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT COUNT(*) FROM messages')
    count = cursor.fetchone()[0]
    conn.close()
    return count