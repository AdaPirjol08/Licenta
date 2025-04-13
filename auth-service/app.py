from flask import Flask, request, jsonify
import sqlite3
import os
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

DB_PATH = "auth.db"

def init_db():
    """Inițializează baza de date dacă nu există."""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                tier TEXT DEFAULT 'free'
            )
        ''')
        conn.commit()
        conn.close()
        print("Baza de date a fost creată.")
    else:
        print(f"Baza de date {DB_PATH} există deja.")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    tier = data.get('tier', 'free')  # Dacă nu se trimite tier, îl setăm default pe 'free'

    # Dacă nu este 'free', considerăm automat ca 'premium'
    if tier != 'free':
        tier = 'premium'

    # Criptarea parolei
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # Inserare user nou în DB
        c.execute('INSERT INTO users (username, password, tier) VALUES (?, ?, ?)',
                  (username, hashed_password, tier))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"message": "Username already exists"}), 400
    conn.close()

    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    """Loghează utilizatorul."""
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, password, tier FROM users WHERE username=?",
              (username,))
    result = c.fetchone()
    conn.close()

    if result:
        user_id, stored_password, tier = result
        # Verifică dacă parola este corectă
        if bcrypt.check_password_hash(stored_password, password):
            return jsonify({"message": "Login success", "user_id": user_id, "tier": tier}), 200
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    init_db()  # Asigură-te că baza de date este creată
    app.run(host='0.0.0.0', port=5001)
