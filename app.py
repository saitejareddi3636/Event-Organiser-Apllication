from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from modules.auth import register_user, login_user, get_password
from modules.events import add_event, get_events, delete_event, mark_favorite, send_message, get_messages

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = login_user(username, password)
        if user_id:
            session['user_id'] = user_id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard', user_id=user_id))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        flash('Username already exists.', 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('Please log in to access your dashboard.', 'warning')
        return redirect(url_for('login'))

    events = get_events(user_id, include_public=True)
    chat_messages = get_messages(user_id, other_user_id=None)  # Fetch chat messages for the user
    return render_template('dashboard.html', events=events, user_id=user_id, chat_messages=chat_messages)

@app.route('/view_event/<int:event_id>')
def view_event(event_id):
    conn = sqlite3.connect("database/event_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT name, date, location, is_public FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    conn.close()
    if event:
        return render_template('view_event.html', event=event)
    flash('Event not found or is private.', 'danger')
    return redirect(url_for('home'))

@app.route('/add_event/<int:user_id>', methods=['POST'])
def add_event_route(user_id):
    name = request.form['name']
    date = request.form['date']
    location = request.form['location']
    is_public = "is_public" in request.form
    add_event(user_id, name, date, location, is_public)
    flash('Event added successfully!', 'success')
    return redirect(url_for('dashboard', user_id=user_id))

@app.route('/send_message/<int:user_id>/<int:other_user_id>', methods=['POST'])
def send_message_route(user_id, other_user_id):
    message = request.form['message']
    send_message(user_id, other_user_id, message)
    flash('Message sent successfully!', 'success')
    return redirect(url_for('dashboard', user_id=user_id))

@app.route('/favorite_event/<int:event_id>/<int:user_id>', methods=['POST'])
def favorite_event(event_id, user_id):
    mark_favorite(event_id)
    flash('Event added to favorites!', 'success')
    return redirect(url_for('dashboard', user_id=user_id))

@app.route('/remove_favorite/<int:event_id>/<int:user_id>', methods=['POST'])
def remove_favorite(event_id, user_id):
    mark_favorite(event_id)
    flash('Event removed from favorites!', 'success')
    return redirect(url_for('dashboard', user_id=user_id))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        password = get_password(username)
        if password:
            flash(f'Your password is: {password}', 'info')
        else:
            flash('Username not found.', 'danger')
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run(debug=True)
