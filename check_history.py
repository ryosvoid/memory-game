import sqlite3

# Path to your database file (adjust if needed)
db_path = "memory.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

def show_table(name):
    print(f"\nTable: {name}")
    try:
        for row in cur.execute(f"SELECT * FROM {name}"):
            print(row)
    except Exception as e:
        print("Error:", e)

tables = ["themes", "difficultes", "parties_jouees", "scores_parties"]

for t in tables:
    show_table(t)

conn.close()