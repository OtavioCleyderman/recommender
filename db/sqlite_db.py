import json
import sqlite3
from db.interfaces import DatabaseInterface
from models.user import User
from models.content import Content
from models.interaction import Interaction
from typing import List
from datetime import datetime

class SQLiteDatabase(DatabaseInterface):
    def __init__(self, db_path="recommender.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def _create_tables(self):
        with self.conn:
            self.conn.executescript(open("schema.sql").read())
            self._run_migrations()

    def add_user(self, user: User):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO users (id, name, email, interest_profile) VALUES (?, ?, ?, ?)",
                (user.id, user.name, user.email, json.dumps(user.interest_profile)),
            )

    def get_user(self, user_id: int) -> User:
        cursor = self.conn.execute("SELECT id, name, email, interest_profile FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        user = User(row[0], row[1], row[2])
        user.interest_profile = json.loads(row[3]) if row[3] else {}
        return user

    def list_users(self) -> List[User]:
        cursor = self.conn.execute("SELECT id, name, email FROM users")
        return [User(*row) for row in cursor.fetchall()]

    def add_content(self, content: Content):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO contents (id, title, category, tags, popularity, date_added) VALUES (?, ?, ?, ?, ?, ?)",
                (content.id, content.title, content.category, ",".join(content.tags), content.popularity, content.date_added),
            )

    def list_contents(self) -> List[Content]:
        cursor = self.conn.execute("SELECT id, title, category, tags, popularity FROM contents")
        return [Content(*row) for row in cursor.fetchall()]

    def add_interaction(self, interaction: Interaction):
        with self.conn:
            # Grava a interação
            self.conn.execute(
                "INSERT INTO interactions (user_id, content_id, interaction_type) VALUES (?, ?, ?)",
                (interaction.user_id, interaction.content_id, interaction.interaction_type),
            )

            # Atualiza popularidade do conteúdo
            weight = {
                "view": 1,
                "like": 3,
                "save": 2,
                "share": 5
            }.get(interaction.interaction_type, 0)

            if weight > 0:
                self.conn.execute(
                    "UPDATE contents SET popularity = popularity + ? WHERE id = ?",
                    (weight, interaction.content_id)
                )

            # Atualiza interesse do usuário
            content_cursor = self.conn.execute(
                "SELECT category FROM contents WHERE id = ?", (interaction.content_id,)
            )
            content_row = content_cursor.fetchone()
            if content_row:
                category = content_row[0]
                user = self.get_user(interaction.user_id)
                if user:
                    user.interest_profile[category] = user.interest_profile.get(category, 0) + 1
                    self.add_user(user)  # regrava com novo perfil

    def list_interactions(self, user_id: int) -> List[Interaction]:
        cursor = self.conn.execute("SELECT id, user_id, content_id, interaction_type FROM interactions")
        return [Interaction(*row) for row in cursor.fetchall()]

    def get_interactions(self, content_id: int) -> List[Interaction]:
        cursor = self.conn.execute(
            "SELECT user_id, content_id, interaction_type FROM interactions WHERE content_id = ?",
            (content_id,)
        )
        return [Interaction(id, user_id, content_id, interaction_type) for user_id, content_id, interaction_type in cursor.fetchall()]

    def get_all_contents(self):
        self.cursor.execute("SELECT * FROM contents")
        rows = self.cursor.fetchall()
        contents = []
        for row in rows:
            content = Content(row[0], row[1], row[2], row[3].split(","))
            contents.append(content)
        return contents

    def get_all_interactions(self):
        self.cursor.execute("SELECT * FROM interactions")
        rows = self.cursor.fetchall()
        interactions = []
        for row in rows:
            interaction = Interaction(row[0], row[1], row[2], row[3])
            interactions.append(interaction)
        return interactions

    def _run_migrations(self):
        with self.conn:
            # Cria tabela de log de migrações se não existir
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS migrations_applied (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    applied_at TEXT
                )
            """)

            # Lista de migrações que podemos aplicar
            migrations = [
                {
                    "name": "add_interest_profile_to_users",
                    "sql": "ALTER TABLE users ADD COLUMN interest_profile TEXT"
                },
                # futuras migrações entram aqui!
            ]

            for mig in migrations:
                # Verifica se a migração já foi aplicada
                result = self.conn.execute("SELECT 1 FROM migrations_applied WHERE name = ?", (mig["name"],)).fetchone()
                if not result:
                    print(f"🛠️  Aplicando migração: {mig['name']}")
                    self.conn.execute(mig["sql"])
                    self.conn.execute(
                        "INSERT INTO migrations_applied (name, applied_at) VALUES (?, ?)",
                        (mig["name"], datetime.utcnow().isoformat())
                    )
