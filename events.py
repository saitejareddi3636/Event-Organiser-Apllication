import sqlite3

def get_messages(user_id, other_user_id):
    conn = sqlite3.connect("database/event_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender_id, receiver_id, message, timestamp
        FROM chats
        WHERE (sender_id = ? AND receiver_id = ?)
        OR (sender_id = ? AND receiver_id = ?)
        ORDER BY timestamp
    """, (user_id, other_user_id, other_user_id, user_id))
    messages = cursor.fetchall()
    conn.close()
    return messages

def send_message(sender_id, receiver_id, message):
    conn = sqlite3.connect("database/event_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chats (sender_id, receiver_id, message)
        VALUES (?, ?, ?)
    """, (sender_id, receiver_id, message))
    conn.commit()
    conn.close()

def add_event(user_id, name, date, location, is_public=False):
    conn = sqlite3.connect("database/event_db.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (user_id, name, date, location, is_favorite, is_public) VALUES (?, ?, ?, ?, 0, ?)",
        (user_id, name, date, location, 1 if is_public else 0),
    )
    conn.commit()
    conn.close()

def get_events(user_id, include_public=True):
    conn = sqlite3.connect("database/event_db.sqlite")
    cursor = conn.cursor()
    if include_public:
        cursor.execute(
            "SELECT id, name, date, location, is_favorite, is_public FROM events WHERE user_id = ? OR is_public = 1",
            (user_id,),
        )
    else:
        cursor.execute(
            "SELECT id, name, date, location, is_favorite, is_public FROM events WHERE user_id = ?",
            (user_id,),
        )
    events = cursor.fetchall()
    conn.close()
    return events

def mark_favorite(event_id):
    conn = sqlite3.connect("database/event_db.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE events SET is_favorite = CASE WHEN is_favorite = 0 THEN 1 ELSE 0 END WHERE id = ?",
        (event_id,),
    )
    conn.commit()
    conn.close()
