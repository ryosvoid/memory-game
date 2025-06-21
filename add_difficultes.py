import sqlite3

conn = sqlite3.connect("memory.db")
cur = conn.cursor()
difficultes = [
    ("2x2", "Très facile", 2, 2, None),
    ("2x3", "Facile", 2, 3, None),
    ("4x4", "Normal", 4, 4, None),
    ("4x5", "Difficile", 4, 5, None),
    ("6x6", "Expert", 6, 6, None),
    ("8x8", "Légendaire", 8, 8, None),
]
for code, label, nb_lignes, nb_colonnes, temps_limite in difficultes:
    cur.execute(
        "INSERT OR IGNORE INTO difficultes (code, label, nb_lignes, nb_colonnes, temps_limite) VALUES (?, ?, ?, ?, ?)",
        (code, label, nb_lignes, nb_colonnes, temps_limite)
    )
conn.commit()
conn.close()
print("Difficultés ajoutées avec toutes les colonnes requises !")