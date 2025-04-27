from typing import List
from models.interaction import Interaction
from datetime import datetime


class Content:
    def __init__(self, content_id: int, title: str, category: str, tags: List[str], popularity=0, date_added: datetime = None):
        self.id = content_id
        self.title = title
        self.category = category
        self.tags = tags
        self.popularity = popularity
        self.date_added = date_added or datetime.now()

    def apply_interaction(self, interaction: object):
        if not isinstance(interaction, Interaction):
            raise ValueError("Objeto inválido: precisa ser uma instância de Interaction")
        
        interaction_scores = {
            'view': 1,
            'like': 3,
            'save': 2,
            'share': 5
        }

        score = interaction_scores.get(interaction.interaction_type)

        if score:
            self.popularity += score
        else:
            print(f"Ignorando tipo não reconhecido: {interaction.interaction_type}")


    def __repr__(self):
        return f"Content({self.content_id}, {self.title}, {self.category})"