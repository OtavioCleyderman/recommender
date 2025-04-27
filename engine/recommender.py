from models.user import User
from models.content import Content
from db.database import MockDatabase
from datetime import datetime, timedelta

class RecommendationEngine:
    def __init__(self, db: MockDatabase):
        self.db = db
    
    def calculate_relevance(self, content: Content, user: User, interaction_weight: float): 
        popularity = content.popularity
        print(f"Calculando relevância para o conteúdo: {content.title}")
        print(f"  Popularidade: {popularity}, Peso de interação: {interaction_weight}")


        user_interest = user.interest_profile.get(content.category, 0)
        print(f"  Interesse do usuário na categoria {content.category}: {user_interest}")


        relevance = (popularity * interaction_weight) + user_interest
        print(f"  Relevância inicial (Popularidade * Peso de interação + Interesse): {relevance}")
        

        days_since_added = (datetime.now() - content.date_added).days
        if days_since_added <= 7:  # Conteúdos adicionados nos últimos 7 dias
            relevance += 0.5
            print(f"  Reforço para conteúdo recente: +0.5")


        if content.category not in user.interest_profile:
            relevance += 1
            print(f"  Reforço para categorias novas: +1")

        print(f"  Relevância final: {relevance}")
        return relevance

    
    def get_recommendations(self, user: User):

        contents = self.db.get_all_contents()
        

        interaction_weights = {
            'view': 0.5,
            'like': 1,
            'save': 2,
            'share': 3
        }
        
        recommendations = []
        

        user_interactions = {interaction.content_id for interaction in self.db.list_interactions(user.id)}
        

        for content in contents:
            if content.id in user_interactions:
                print(f"Ignorando conteúdo já interagido: {content.title}")  # Para debug
                continue  # Pular o conteúdo se o usuário já tiver interagido com ele

            total_relevance = 0
            interactions = self.db.get_interactions(content.id)
            for interaction in interactions:
                if interaction.user_id == user.id and interaction.interaction_type in interaction_weights:
                    weight = interaction_weights.get(interaction.interaction_type, 0)
                    relevance = self.calculate_relevance(content, user, weight)
                    total_relevance += relevance

            if total_relevance > 0:
                recommendations.append((content, total_relevance))

        recommendations.sort(key=lambda x: x[1], reverse=True)

        return recommendations
    
    def recommend(self, user_id: int, limit: int = 5) -> list[Content]:
        user = self.db.get_user(user_id)
        if not user:
            print(f"Usuário {user_id} não encontrado.")
            return []

        contents = self.db.contents.values()

        def score(content: Content):
            interest = user.interest_profile.get(content.category, 0)
            popularity = content.popularity
            return (interest * 2) + popularity  # peso maior para interesse

        ranked_contents = sorted(contents, key=score, reverse=True)
        return ranked_contents[:limit]
