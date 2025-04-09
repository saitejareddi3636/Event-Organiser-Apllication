import sqlite3
import os

# Define the database path
db_path = os.path.join(os.path.dirname(__file__), "event_db.sqlite")

def setup_database():
    """
    Create necessary tables and columns in the database if they don't exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Create events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        location TEXT NOT NULL,
        is_favorite INTEGER DEFAULT 0,
        is_public INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    print("Database setup completed successfully!")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
