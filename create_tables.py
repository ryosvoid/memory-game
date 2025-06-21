import sqlite3

db_path = "memory.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Themes table
cur.execute("""
CREATE TABLE IF NOT EXISTS themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE NOT NULL
);
""")

# Difficultés table
cur.execute("""
CREATE TABLE IF NOT EXISTS difficultes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    label TEXT NOT NULL
);
""")

# Utilisateurs table
cur.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
""")

# Parties jouées table
cur.execute("""
CREATE TABLE IF NOT EXISTS parties_jouees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme_id INTEGER,
    difficulte_id INTEGER,
    mode_multijoueur INTEGER,
    duree_seconds INTEGER,
    gagnant_id INTEGER,
    date_partie TEXT,
    FOREIGN KEY(theme_id) REFERENCES themes(id),
    FOREIGN KEY(difficulte_id) REFERENCES difficultes(id),
    FOREIGN KEY(gagnant_id) REFERENCES utilisateurs(id)
);
""")

# Scores parties table
cur.execute("""
CREATE TABLE IF NOT EXISTS scores_parties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partie_id INTEGER,
    utilisateur_id INTEGER,
    score INTEGER,
    coups INTEGER,
    FOREIGN KEY(partie_id) REFERENCES parties_jouees(id),
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id)
);
""")

conn.commit()
conn.close()
print("Tables created!")