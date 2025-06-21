import sqlite3

db_path = "memory.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

themes = ["Fruits", "Drinks", "Food", "Flowers", "Bakery"]
for t in themes:
    cur.execute("INSERT OR IGNORE INTO themes (nom) VALUES (?)", (t,))
conn.commit()
conn.close()

print("Themes added!")