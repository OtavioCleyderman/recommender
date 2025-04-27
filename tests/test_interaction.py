from models.interaction import Interaction

def test_interaction_fields():
    interaction = Interaction(1, 1, 2, "like")
    assert interaction.id == 1
    assert interaction.user_id == 1
    assert interaction.content_id == 2
    assert interaction.interaction_type == "like"
