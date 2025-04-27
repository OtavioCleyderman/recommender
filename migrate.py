# migrate.py
import os
import sqlite3
from db.migrator import Migrator

DB_PATH = "recommender.db"

def main():
    creating_db = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    if creating_db:
        print("📄 Criando estrutura inicial do banco com schema.sql...")
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())

    migrator = Migrator(conn)
    migrator.run_migrations()
    conn.close()

if __name__ == "__main__":
    main()
