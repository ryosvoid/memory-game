import sqlite3

DB_FILE = "memory.db"
SCHEMA_FILE = "schema_memory.sql"

def init_db():
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema = f.read()
    conn = sqlite3.connect(DB_FILE)
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("Database installed :)")

if __name__ == "__main__":
    init_db()
