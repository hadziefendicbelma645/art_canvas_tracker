from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_FILE = "tasks.db"

def init_db():
    """Funkcija koja kreira tabelu u bazi ako već ne postoji."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'U toku'
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Prikaz svih zadataka iz baze podataka."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    all_tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=all_tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Dodavanje novog zadatka u bazu."""
    task_title = request.form.get('title')
    if task_title:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task_title,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Brisanje zadatka iz baze."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Inicijalizacija baze prije pokretanja
    app.run(host='0.0.0.0', port=5000, debug=True)
