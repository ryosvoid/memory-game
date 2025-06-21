CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(40) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS difficultes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(10) UNIQUE NOT NULL, -- ex: '2x2'
    label VARCHAR(40) NOT NULL,       -- ex: 'Très facile'
    nb_lignes INTEGER NOT NULL,
    nb_colonnes INTEGER NOT NULL,
    temps_limite INTEGER
);

CREATE TABLE IF NOT EXISTS themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(40) UNIQUE NOT NULL,
    image_url VARCHAR(250)
);

CREATE TABLE IF NOT EXISTS parties_jouees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme_id INTEGER NOT NULL,
    difficulte_id INTEGER NOT NULL,
    mode_multijoueur BOOLEAN NOT NULL,
    date_partie DATETIME DEFAULT CURRENT_TIMESTAMP,
    gagnant_id INTEGER,
    duree_seconds INTEGER,
    FOREIGN KEY (theme_id) REFERENCES themes(id),
    FOREIGN KEY (difficulte_id) REFERENCES difficultes(id),
    FOREIGN KEY (gagnant_id) REFERENCES utilisateurs(id)
);

CREATE TABLE IF NOT EXISTS scores_parties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partie_id INTEGER NOT NULL,
    utilisateur_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    est_gagnant BOOLEAN,
    nombre_mouvements INTEGER,
    FOREIGN KEY (partie_id) REFERENCES parties_jouees(id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
);

-- Default difficulties
INSERT OR IGNORE INTO difficultes (code, label, nb_lignes, nb_colonnes, temps_limite) VALUES
('2x2', 'Très facile', 2, 2, 20),
('2x3', 'Facile', 2, 3, 28),
('4x4', 'Normal', 4, 4, 56),
('4x5', 'Difficile', 4, 5, 70),
('6x6', 'Expert', 6, 6, 110),
('8x8', 'Légendaire', 8, 8, 200);

-- Default themes
INSERT OR IGNORE INTO themes (nom) VALUES ('Fruits'), ('Drinks'), ('Food'), ('Flowers'), ('Bakery');