# main.py
from db.database import MockDatabase
from models.user import User
from models.content import Content
from models.interaction import Interaction
from engine.recommender import RecommendationEngine
from db.database import MockDatabase
from db.interfaces import DatabaseInterface
from db.sqlite_db import SQLiteDatabase

# db: DatabaseInterface = MockDatabase()
db = SQLiteDatabase("recommender.db")

# # Criar usuário e conteúdo
user = User(1, "Alice", "alice@example.com")
content = Content(1, "10 dicas de viagem", "viagem", ["aventura", "praia"])
content2 = Content(2, "Como planejar sua viagem dos sonhos", "viagem", ["planejamento", "mochila"])
content3 = Content(3, "Os melhores cafés do Brasil", "gastronomia", ["café", "viagem"])
content4 = Content(4, "Top 10 séries de suspense", "entretenimento", ["suspense", "drama"])
content5 = Content(5, "Guia de meditação para iniciantes", "bem-estar", ["relaxamento", "autoajuda"])

db.add_user(user)
db.add_content(content)
db.add_content(content2)
db.add_content(content3)
db.add_content(content4)
db.add_content(content5)

interaction = Interaction(1, user_id=1, content_id=1, interaction_type="like")
db.add_interaction(interaction)
interaction = Interaction(1, user_id=1, content_id=1, interaction_type="save")
db.add_interaction(interaction)

interaction3 = Interaction(3, user_id=1, content_id=3, interaction_type="save")
db.add_interaction(interaction3)

# Criar a engine de recomendação
recommender = RecommendationEngine(db)

# Obter recomendações para o usuário
recommendations = recommender.get_recommendations(user)

# Exibir as recomendações
print(f"📢 Recomendações para o usuário {user.name}:\n")
for content, relevance in recommendations:
    print(f"- {content.title} (Categoria: {content.category}, Relevância: {relevance})")

# Caso queira verificar se algum conteúdo foi pulado, pode também imprimir o conteúdo ignorado:
all_content_ids = {content.id for content in [content, content2, content3, content4, content5]}
recommended_content_ids = {content.id for content, _ in recommendations}

ignored_content_ids = all_content_ids - recommended_content_ids
if ignored_content_ids:
    print(f"\nConteúdos ignorados (já interagidos): {ignored_content_ids}")
