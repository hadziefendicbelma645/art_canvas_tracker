from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import time

app = Flask(__name__)


DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "art_db")
DB_USER = os.environ.get("DB_USER", "belma")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "sigurnasifra123")

def get_db_connection():
    """Funkcija koja pokušava da se poveže na PostgreSQL bazu podataka."""
   
    for _ in range(5):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError:
            time.sleep(2)
    raise Exception("Nije moguće povezivanje na PostgreSQL bazu podataka.")

def init_db():
    """Kreiranje tabele za umjetničke slike ako ne postoji."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artworks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            technique VARCHAR(255) NOT NULL,
            status VARCHAR(50) DEFAULT 'U planu'
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    """Prikaz svih slika iz baze podataka."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artworks")
    all_artworks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', artworks=all_artworks)

@app.route('/add', methods=['POST'])
def add_artwork():
    """Dodavanje nove slike u evidenciju."""
    title = request.form.get('title')
    technique = request.form.get('technique')
    if title and technique:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO artworks (title, technique) VALUES (%s, %s)",
            (title, technique)
        )
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:art_id>')
def delete_artwork(art_id):
    """Brisanje slike iz baze."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM artworks WHERE id = %s", (art_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
