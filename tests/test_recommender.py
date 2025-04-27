from models.user import User
from models.content import Content
from models.interaction import Interaction
from db.database import MockDatabase
from engine.recommender import RecommendationEngine

def test_recommendation_flow():
    db = MockDatabase()
    user = User(1, "Alice", "alice@example.com")
    db.add_user(user)

    content1 = Content(1, "Post 1", "viagem", [])
    content2 = Content(2, "Post 2", "gastronomia", [])
    db.add_content(content1)
    db.add_content(content2)

    interaction = Interaction(1, user_id=1, content_id=1, interaction_type="like")
    db.add_interaction(interaction)

    engine = RecommendationEngine(db)
    results = engine.recommend(user_id=1)

    assert results[0].id == 1  # conteúdo da categoria "viagem" que teve interação
