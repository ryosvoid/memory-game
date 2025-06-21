CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS difficultes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    label TEXT NOT NULL
);

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

CREATE TABLE IF NOT EXISTS scores_parties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partie_id INTEGER,
    utilisateur_id INTEGER,
    score INTEGER,
    FOREIGN KEY(partie_id) REFERENCES parties_jouees(id),
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id)
);

-- Pre-fill for themes and difficulties
INSERT OR IGNORE INTO themes (nom) VALUES
('Fruits'), ('Drinks'), ('Food'), ('Flowers'), ('Bakery');

INSERT OR IGNORE INTO difficultes (code, label) VALUES
('2x2', 'Très facile'),
('2x3', 'Facile'),
('4x4', 'Normal'),
('4x5', 'Difficile'),
('6x6', 'Expert'),
('8x8', 'Légendaire');
