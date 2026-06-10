from flask import Flask, render_template, request, redirect
from database import init_db, get_all_messages, add_message, delete_message, get_message_count
from datetime import date
import sqlite3

app = Flask(__name__)

DB_NAME = 'guestbook.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    messages = get_all_messages()
    total_count = get_message_count()
    today = date.today().isoformat()
    return render_template('index.html', messages=messages, total_count=total_count, today=today)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    message = request.form['message']
    add_message(name, message)
    return redirect('/')

@app.route('/delete/<int:message_id>')
def delete(message_id):
    delete_message(message_id)
    return redirect('/')

@app.route('/sort/newest')
def sort_newest():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY created_at DESC').fetchall()
    conn.close()
    total_count = len(messages)
    today = date.today().isoformat()
    return render_template('index.html', messages=messages, total_count=total_count, today=today)

@app.route('/sort/oldest')
def sort_oldest():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY created_at ASC').fetchall()
    conn.close()
    total_count = len(messages)
    today = date.today().isoformat()
    return render_template('index.html', messages=messages, total_count=total_count, today=today)

@app.route('/delete-all')
def delete_all():
    return render_template('delete_all.html')

@app.route('/delete-all-confirm', methods=['POST'])
def delete_all_confirm():
    conn = get_db_connection()
    conn.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)