import sqlite3

conn = sqlite3.connect("memory.db")
cur = conn.cursor()
for row in cur.execute("SELECT id, code, label FROM difficultes"):
    print(row)
conn.close()