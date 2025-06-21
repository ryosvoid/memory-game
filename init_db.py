import sqlite3

with open('schema_memory.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

conn = sqlite3.connect('memory.db')
conn.executescript(sql)
conn.commit()
conn.close()
print("Database initialized!")