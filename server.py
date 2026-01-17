#!/usr/bin/env python3
"""Simple HTTP server using Python built-in modules (no Flask required)"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
HOST = '0.0.0.0'
PORT = 5000


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


FORM_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add User</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        form { display: flex; flex-direction: column; gap: 15px; }
        label { font-weight: bold; }
        input { padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 20px; font-size: 16px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        a { display: inline-block; margin-top: 20px; color: #007bff; }
    </style>
</head>
<body>
    <h1>Add User</h1>
    <form method="POST">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <label for="age">Age:</label>
        <input type="number" id="age" name="age" required min="1">
        <button type="submit">Save</button>
    </form>
    <a href="/users">View All Users</a>
</body>
</html>'''


def render_users_page(users):
    if users:
        rows = ''.join(f'<tr><td>{u["id"]}</td><td>{u["name"]}</td><td>{u["age"]}</td></tr>' for u in users)
        table = f'''<table>
        <thead><tr><th>ID</th><th>Name</th><th>Age</th></tr></thead>
        <tbody>{rows}</tbody>
        </table>'''
    else:
        table = '<p class="empty">No users found.</p>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Users</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #007bff; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
        a {{ display: inline-block; margin-top: 20px; color: #007bff; }}
        .empty {{ color: #666; font-style: italic; }}
    </style>
</head>
<body>
    <h1>All Users</h1>
    {table}
    <a href="/">Add New User</a>
</body>
</html>'''


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(FORM_HTML.encode())
        elif self.path == '/users':
            with get_db() as conn:
                users = conn.execute('SELECT * FROM users').fetchall()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(render_users_page(users).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            name = params.get('name', [''])[0]
            age = params.get('age', [''])[0]
            if name and age:
                with get_db() as conn:
                    conn.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
                    conn.commit()
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {args[0]}")


if __name__ == '__main__':
    init_db()
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f' * Running on http://{HOST}:{PORT}')
    print(f' * Open http://localhost:{PORT} in your browser')
    print(' * Press Ctrl+C to stop')
    server.serve_forever()
