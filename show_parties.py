import sqlite3

conn = sqlite3.connect('memory.db')
cursor = conn.cursor()
try:
    for row in cursor.execute('SELECT * FROM parties_jouees'):
        print(row)
except Exception as e:
    print("Erreur lors de la lecture :", e)
conn.close()