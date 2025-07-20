from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'database.db'

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
        ''')
        conn.commit()
        conn.close()
        print("✅ Tạo file database và bảng users thành công.")
    else:
        print("ℹ️ Database đã tồn tại.")

def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = connect_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        conn = connect_db()
        conn.execute('INSERT INTO users (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = connect_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        new_name = request.form['name']
        conn.execute('UPDATE users SET name = ? WHERE id = ?', (new_name, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('edit.html', user=user)

@app.route('/delete/<int:id>')
def delete(id):
    conn = connect_db()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
