from datetime import datetime, timedelta
from plyer import notification
import sqlite3

def check_for_upcoming_events(user_id):
    conn = sqlite3.connect("database/event_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT name, date FROM events WHERE user_id = ?", (user_id,))
    events = cursor.fetchall()
    conn.close()

    for event in events:
        event_date = datetime.strptime(event[1], "%Y-%m-%d")
        if 0 <= (event_date - datetime.now()).days < 1:
            notification.notify(
                title="Event Reminder",
                message=f"Upcoming Event: {event[0]} on {event[1]}",
                timeout=10
            )
