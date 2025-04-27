from db.interfaces import DatabaseInterface
from typing import Dict, List
from models.user import User
from models.content import Content
from models.interaction import Interaction

class MockDatabase(DatabaseInterface):

    def __init__(self):
        self.users: Dict[int, User] = {}
        self.contents: Dict[int, Content] = {}
        self.interactions: List[Interaction] = []

    def add_user(self, user: User):
        self.users[user.id] = user

    def get_user(self, user_id: int) -> User:
        return self.users[user_id]

    def list_users(self) -> List[User]:
        return list(self.users.values())

    def add_content(self, content: Content):
        self.contents[content.id] = content

    def list_contents(self) -> List[Content]:
        return list(self.contents.values())

    def add_interaction(self, interaction: Interaction):
        self.interactions.append(interaction)
        content = self.contents.get(interaction.content_id)
        if content:
            content.apply_interaction(interaction)
        user = self.users.get(interaction.user_id)
        if user and content:
            user.update_interest(content.category, 1)

    def list_interactions(self) -> List[Interaction]:
        return self.interactions
