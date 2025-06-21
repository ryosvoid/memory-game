import sqlite3

conn = sqlite3.connect('memory.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(parties_jouees)")
for col in cursor.fetchall():
    print(col)
conn.close()