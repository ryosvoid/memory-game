import sqlite3
conn = sqlite3.connect("memory.db")
cur = conn.cursor()
cur.execute("PRAGMA table_info(difficultes);")
print("Schema:", cur.fetchall())
conn.close()