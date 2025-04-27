from abc import ABC, abstractmethod
from typing import List
from models.user import User
from models.content import Content
from models.interaction import Interaction

class DatabaseInterface(ABC):

    @abstractmethod
    def add_user(self, user: User): pass

    @abstractmethod
    def get_user(self, user_id: int) -> User: pass

    @abstractmethod
    def add_content(self, content: Content): pass

    @abstractmethod
    def list_contents(self) -> List[Content]: pass

    @abstractmethod
    def add_interaction(self, interaction: Interaction): pass

    @abstractmethod
    def list_users(self) -> List[User]: pass

    @abstractmethod
    def list_interactions(self) -> List[Interaction]: pass
