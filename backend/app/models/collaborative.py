import pandas as pd
import numpy as np
import scipy.sparse as sparse
import implicit
import os
from app.config import settings

class FoodRecommender:
    def __init__(self):
        self.model = None
        self.user_mapping = {}
        self.item_mapping = {}

    def train(self):
        df = pd.read_csv(os.path.join(settings.GENERATED_DATA_DIR, "user_food_preferences.csv"))
        
        users = df['user_hash'].astype("category")
        items = df['dish_name'].astype("category")
        
        self.user_mapping = dict(enumerate(users.cat.categories))
        self.item_mapping = dict(enumerate(items.cat.categories))
        self.rev_item_mapping = {v: k for k, v in self.item_mapping.items()}
        
        row = users.cat.codes
        col = items.cat.codes
        data = df['avg_rating'].values * df['interaction_count'].values
        
        sparse_item_user = sparse.csr_matrix((data, (col, row)))
        
        self.model = implicit.als.AlternatingLeastSquares(factors=20, regularization=0.1, iterations=20, random_state=42)
        self.model.fit(sparse_item_user)

    def _load_model(self):
        if not self.model:
            self.train()

    def get_popularity_adjustment(self, menu_items, user_segment=None):
        return {item['name']: item.get('popularity_score', 0.8) for item in menu_items}

    def predict_menu_demand_factor(self, menu_items):
        self._load_model()
        if not menu_items: return 1.0
        
        scores = []
        for item in menu_items:
            idx = self.rev_item_mapping.get(item['name'])
            if idx is not None:
                # Approximate overall appeal using item factors
                factor_norm = np.linalg.norm(self.model.item_factors[idx])
                scores.append(factor_norm)
        
        if not scores: return 1.0
        avg_score = sum(scores) / len(scores)
        # Scale to a multiplier around 1.0
        return min(max(avg_score * 0.1, 0.7), 1.3)
