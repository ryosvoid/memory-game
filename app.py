from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
import os
import random
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "memorysecret"
app.permanent_session_lifetime = timedelta(hours=2)

DATABASE = "memory.db"

def init_db():
    """Initialize the database if it doesn't exist or is corrupted."""
    need_init = False
    if not os.path.exists(DATABASE):
        need_init = True
    else:
        try:
            conn = sqlite3.connect(DATABASE)
            conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            conn.close()
        except sqlite3.DatabaseError:
            os.remove(DATABASE)
            need_init = True

    if need_init:
        with open("schema.sql", "r", encoding="utf-8") as f:
            schema = f.read()
        conn = sqlite3.connect(DATABASE)
        conn.executescript(schema)
        conn.commit()
        conn.close()
        print("Database initialized!")

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_user_id(username):
    cur = get_db().execute("SELECT id FROM utilisateurs WHERE username = ?", (username,))
    row = cur.fetchone()
    return row['id'] if row else None

THEMES = ["Fruits", "Drinks", "Food", "Flowers", "Bakery"]

DIFFICULTY_GRIDS = {
    "2x2": (2, 2),
    "2x3": (2, 3),
    "4x4": (4, 4),
    "4x5": (4, 5),
    "6x6": (6, 6),
    "8x8": (8, 8)
}

DIFFICULTY_LABELS = {
    "2x2": "Très facile",
    "2x3": "Facile",
    "4x4": "Normal",
    "4x5": "Difficile",
    "6x6": "Expert",
    "8x8": "Légendaire"
}

DEFAULT_DIFFICULTY = "4x4"

@app.before_first_request
def before_first_request():
    init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        action = request.form.get('action')
        db = get_db()
        if not username or not password:
            error = "Please fill all fields."
        elif action == "Login":
            cur = db.execute("SELECT * FROM utilisateurs WHERE username=? AND password_hash=?", (username, password))
            user = cur.fetchone()
            if user:
                session['username'] = username
                session['score'] = 100
                return redirect(url_for('theme_select'))
            else:
                error = "Invalid credentials."
        elif action == "Register":
            cur = db.execute("SELECT id FROM utilisateurs WHERE username=?", (username,))
            if cur.fetchone():
                error = "Username already exists."
            else:
                db.execute("INSERT INTO utilisateurs (username, password_hash) VALUES (?, ?)", (username, password))
                db.commit()
                session['username'] = username
                session['score'] = 100
                return redirect(url_for('theme_select'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/themes')
def theme_select():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template(
        "index.html",
        themes=THEMES,
        DIFFICULTY_LABELS=DIFFICULTY_LABELS
    )

@app.route('/historique')
def historique():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id(session['username'])
    cur = get_db().execute("""
        SELECT pj.id, pj.date_partie, th.nom as theme, d.label as difficulte,
               pj.mode_multijoueur, pj.duree_seconds, u.username as gagnant
        FROM parties_jouees pj
        JOIN themes th ON pj.theme_id = th.id
        JOIN difficultes d ON pj.difficulte_id = d.id
        LEFT JOIN utilisateurs u ON pj.gagnant_id = u.id
        WHERE pj.id IN (
            SELECT partie_id FROM scores_parties WHERE utilisateur_id = ?
        )
        ORDER BY pj.date_partie DESC
        LIMIT 20
        """, (user_id,))
    parties = cur.fetchall()
    return render_template('historique.html', parties=parties)

@app.route('/game/<theme>')
def game(theme):
    if 'username' not in session:
        return redirect(url_for('login'))
    session.permanent = True

    difficulty = request.args.get('difficulty', DEFAULT_DIFFICULTY)
    is_multiplayer = request.args.get('multiplayer') == '1'

    rows, cols = DIFFICULTY_GRIDS.get(difficulty, DIFFICULTY_GRIDS[DEFAULT_DIFFICULTY])
    total_cards = rows * cols
    if total_cards % 2 != 0:
        total_cards -= 1
    pairs = total_cards // 2

    theme_folder = os.path.join("static", "images", theme.lower())
    if not os.path.exists(theme_folder):
        return "Invalid theme folder."
    all_images = [f for f in os.listdir(theme_folder) if f.endswith(".jpg")]

    # --- Flexible image selection logic ---
    if difficulty in ("6x6", "8x8"):
        if len(all_images) == 0:
            return "No images in the theme folder."
        # For 6x6 and 8x8, repeat images as needed
        selected_images = [all_images[i % len(all_images)] for i in range(pairs)]
    else:
        if len(all_images) < pairs:
            return "Not enough images in the theme folder for this level."
        selected_images = random.sample(all_images, pairs)
    card_images = selected_images * 2
    random.shuffle(card_images)

    if is_multiplayer:
        if (session.get('multi_theme') != theme or session.get('multi_diff') != difficulty):
            session['multi_theme'] = theme
            session['multi_diff'] = difficulty
            session['multi_scores'] = [0, 0]
            session['multi_player'] = 0
        scores = session['multi_scores']
        current_player = session['multi_player']
    else:
        session.pop('multi_theme', None)
        session.pop('multi_diff', None)
        session.pop('multi_scores', None)
        session.pop('multi_player', None)
        scores = None
        current_player = None

    score = int(session.get('score', 100))
    if difficulty
