from datetime import datetime

class Migrator:
    def __init__(self, conn):
        self.conn = conn

    def _column_exists(self, table, column):
        cursor = self.conn.execute(f"PRAGMA table_info({table})")
        return column in [row[1] for row in cursor.fetchall()]

    def run_migrations(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS migrations_applied (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    applied_at TEXT
                )
            """)

            migrations = [
                {
                    "name": "add_interest_profile_to_users",
                    "check": lambda conn: not self._column_exists("users", "interest_profile"),
                    "sql": "ALTER TABLE users ADD COLUMN interest_profile TEXT"
                },
                 {
                    "name": "add_popularity_default_0_to_contents",
                    "check": lambda conn: not self._column_exists("contents", "popularity"),
                    "sql": "ALTER TABLE users ADD COLUMN popularity INTEGER DEFAULT 0"
                },
                # novas migrações vão aqui
            ]

            for mig in migrations:
                result = self.conn.execute("SELECT 1 FROM migrations_applied WHERE name = ?", (mig["name"],)).fetchone()
                should_run = not result and mig["check"](self.conn)

                if should_run:
                    print(f"🛠️  Aplicando migração: {mig['name']}")
                    self.conn.execute(mig["sql"])
                    self.conn.execute(
                        "INSERT INTO migrations_applied (name, applied_at) VALUES (?, ?)",
                        (mig["name"], datetime.utcnow().isoformat())
                    )
                else:
                    print(f"✅ Migração ignorada (já aplicada ou não necessária): {mig['name']}")
