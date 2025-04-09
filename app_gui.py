import sqlite3
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from plyer import notification  # For notifications
from datetime import datetime, timedelta  # For date handling
import csv  # For exporting events
from app import setup_database, add_to_favorites, get_favorites

# Global variable to track logged-in user
current_user_id = None  


def register_user(username, password):
    """Registers a new user."""
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()


def login_user(username, password, root):
    """Logs in an existing user."""
    global current_user_id
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        current_user_id = user[0]
        messagebox.showinfo("Success", "Login successful!")
        root.destroy()
        open_event_manager()
    else:
        messagebox.showerror("Error", "Invalid credentials.")


def open_login_screen():
    """Displays the login and registration screen with modern design."""
    root = ttk.Window(themename="darkly")
    root.title("Event Organizer - Login")

    ttk.Label(root, text="Event Organizer", font=("Helvetica", 18, "bold")).pack(pady=10)
    
    ttk.Label(root, text="Username:", font=("Helvetica", 12)).pack(pady=5)
    username_entry = ttk.Entry(root, bootstyle=INFO)
    username_entry.pack(pady=5)

    ttk.Label(root, text="Password:", font=("Helvetica", 12)).pack(pady=5)
    password_entry = ttk.Entry(root, bootstyle=INFO, show="*")
    password_entry.pack(pady=5)

    login_button = ttk.Button(root, text="Login", bootstyle=SUCCESS, command=lambda: login_user(username_entry.get(), password_entry.get(), root))
    login_button.pack(pady=10)

    register_button = ttk.Button(root, text="Register", bootstyle=WARNING, command=lambda: register_user(username_entry.get(), password_entry.get()))
    register_button.pack(pady=10)

    root.mainloop()


def notify_upcoming_events():
    """Notifies the user about events happening in the next 24 hours."""
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    
    # Query for events happening within the next 24 hours
    cursor.execute("SELECT name, date FROM events WHERE date BETWEEN ? AND ?", 
                   (datetime.now().strftime('%Y-%m-%d'), 
                    (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')))
    upcoming_events = cursor.fetchall()
    conn.close()

    if upcoming_events:
        for event in upcoming_events:
            notification.notify(
                title="Upcoming Event Reminder",
                message=f"{event[0]} is scheduled for {event[1]}.",
                timeout=10
            )

# Creats a frame to layout the elements of the manager
def create_frame(container):
    frame = ttk.Frame(container)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=10)
    
    ttk.Label(frame, text="Event Manager", font=("Helvetica", 18, "bold")).grid(column=0, row=0, sticky=tk.W, pady=5, padx=5)

    ttk.Label(frame, text="Event Name:", font=("Helvetica", 12)).grid(column=0, row=1, sticky=tk.W, pady=5, padx=5)
    event_name_entry = ttk.Entry(frame, bootstyle=INFO)
    event_name_entry.grid(column=1, row=1, sticky=tk.W, pady=5, padx=5)

    ttk.Label(frame, text="Event Date (YYYY-MM-DD):", font=("Helvetica", 12)).grid(column=0, row=2, sticky=tk.W, pady=5, padx=5)
    event_date_entry = ttk.Entry(frame, bootstyle=INFO)
    event_date_entry.grid(column=1, row=2, sticky=tk.W, pady=5, padx=5)

    ttk.Label(frame, text="Location:", font=("Helvetica", 12)).grid(column=0, row=3, sticky=tk.W, pady=5, padx=5)
    location_entry = ttk.Entry(frame, bootstyle=INFO)
    location_entry.grid(column=1, row=3, sticky=tk.W, pady=5, padx=5)

    add_event_button = ttk.Button(frame, text="Add Event", bootstyle=SUCCESS, command=lambda: add_event(event_name_entry, event_date_entry, location_entry))
    add_event_button.grid(column=0, row=4, sticky=tk.W, pady=5, padx=5)

    view_events_button = ttk.Button(frame, text="View Events", bootstyle=INFO, command=view_events)
    view_events_button.grid(column=0, row=5, sticky=tk.W, pady=5, padx=5)

    view_favorites_button = ttk.Button(frame, text="View Favorites", bootstyle=SECONDARY, command=view_favorites)
    view_favorites_button.grid(column=0, row=6, sticky=tk.W, pady=5, padx=5)

    view_shared_button = ttk.Button(frame, text="View Shared Events", bootstyle=PRIMARY, command=view_shared_events)
    view_shared_button.grid(column=0, row=7, sticky=tk.W, pady=5, padx=5)

    export_button = ttk.Button(frame, text="Export Events", bootstyle=INFO)
    export_button.grid(column=0, row=8, sticky=tk.W, pady=5, padx=5)

    return frame

# Opens the event manager when the user logs in
def open_event_manager():
    """Opens the main event manager window and triggers notifications."""
    notify_upcoming_events()  # Notify user about upcoming events

    manager_window = ttk.Window(themename="darkly")
    manager_window.title("Event Organizer - Event Manager")
    manager_window.geometry("900x450")


    manager_window.columnconfigure(0, weight=4)
    manager_window.columnconfigure(1, weight=1)

    input_frame = create_frame(manager_window)
    input_frame.grid(column=0, row=0)

    manager_window.mainloop()

# Adds an event when user enters required information
def add_event(name_entry, date_entry, location_entry):
    """Adds an event to the database."""
    name = name_entry.get()
    date = date_entry.get()
    location = location_entry.get()

    if not name or not date or not location:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Date Error", "Date must be in YYYY-MM-DD format.")
        return

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (name, date, location) VALUES (?, ?, ?)", (name, date, location))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"Event '{name}' added successfully!")
    name_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)

# Opens a new window with the list of events
def view_events():
    """Displays all events in a new window."""
    view_window = ttk.Toplevel()
    view_window.title("View Events")

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()

    if events:
        for event in events:
            event_label = ttk.Label(view_window, text=f"ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Location: {event[3]}")
            event_label.pack()
            favorite_button = ttk.Button(view_window, text="Add to Favorites", bootstyle=SUCCESS, command=lambda e=event[0]: add_to_favorites(current_user_id, e))
            favorite_button.pack()
    else:
        ttk.Label(view_window, text="No events found.", bootstyle=WARNING).pack()

# Views a list of the user's favorited events
def view_favorites():
    """Displays favorite events in a new window."""
    favorites_window = ttk.Toplevel()
    favorites_window.title("Favorite Events")

    favorites_window.protocol("WM_DELETE_WINDOW", lambda: safe_destroy(favorites_window))

    try:
        favorites = get_favorites(current_user_id)
        if favorites:
            for event in favorites:
                ttk.Label(favorites_window, text=f"ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Location: {event[3]}").pack()
        else:
            ttk.Label(favorites_window, text="No favorite events found.", bootstyle=INFO).pack()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def export_events():
    """Exports all events to a CSV file."""
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()

    if events:
        with open('events_export.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Date', 'Location'])
            writer.writerows(events)
        
        messagebox.showinfo("Success", "Events exported to events_export.csv.")
    else:
        messagebox.showerror("Error", "No events found to export.")


def safe_destroy(window):
    """Safely closes windows to avoid resource errors."""
    if window is not None:
        window.destroy()


if __name__ == "__main__":
    setup_database()
    open_login_screen()
