from typing import Dict

class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.id = user_id
        self.name = name
        self.email = email
        self.interest_profile: Dict[str, int] = {} # categoria -> score
    
    def update_interest(self, category: str, score: int):
        """Atualiza o score de interesse do usuário por categoria."""
        self.interest_profile[category] = self.interest_profile.get(category, 0) + score
    
    def reset_interest_profile(self):
        """Reseta o perfil de interesse do usuário (começa do zero)."""
        self.interest_profile.clear()
    
    def __repr__(self):
        return f"User({self.user_id}, {self.name}, {self.email})"