from models.content import Content
from models.interaction import Interaction

def test_popularity_increase():
    content = Content(1, "Post", "viagem", [])
    view = Interaction(1, 1, 1, "view")
    content.apply_interaction(view)
    assert content.popularity == 1
