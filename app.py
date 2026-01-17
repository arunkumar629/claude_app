from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')
        conn.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        with get_db() as conn:
            conn.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('form.html')


@app.route('/users')
def users():
    with get_db() as conn:
        users = conn.execute('SELECT * FROM users').fetchall()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
