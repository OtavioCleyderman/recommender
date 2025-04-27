from datetime import datetime


class Interaction:
    def __init__(self, interaction_id: int, user_id: int, content_id: int, interaction_type: str):
        self.id = interaction_id
        self.user_id = user_id
        self.content_id = content_id
        self.interaction_type = interaction_type  # like, save, view, share
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"Interaction({self.user_id} -> {self.content_id}, {self.interaction_type})"
