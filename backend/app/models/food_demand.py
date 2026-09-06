import xgboost as xgb
import pandas as pd
import joblib
import os
from sklearn.preprocessing import LabelEncoder
from app.config import settings

class FoodDemandPredictor:
    def __init__(self):
        self.model = None
        self.le_meal = LabelEncoder()
        self.le_caf = LabelEncoder()
        self.model_path = os.path.join(settings.MODELS_DIR, "food_xgb.joblib")
        self.features = ['campus_occupancy', 'weekday', 'meal_encoded', 'cafeteria_encoded', 'exam_week', 'temperature', 'rain', 'event_count', 'semester_week', 'menu_popularity_avg']

    def train(self, data_path: str = None):
        if not data_path:
            data_path = os.path.join(settings.GENERATED_DATA_DIR, "cafeteria_sales.csv")
        df = pd.read_csv(data_path)
        df['meal_encoded'] = self.le_meal.fit_transform(df['meal_type'])
        df['cafeteria_encoded'] = self.le_caf.fit_transform(df['cafeteria_id'])
        
        X = df[self.features]
        y = df['portions_sold']
        
        self.model = xgb.XGBRegressor(n_estimators=100, max_depth=4, random_state=42)
        self.model.fit(X, y)
        os.makedirs(settings.MODELS_DIR, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.le_meal, os.path.join(settings.MODELS_DIR, "food_le_meal.joblib"))
        joblib.dump(self.le_caf, os.path.join(settings.MODELS_DIR, "food_le_caf.joblib"))

    def _load_model(self):
        if not self.model:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.le_meal = joblib.load(os.path.join(settings.MODELS_DIR, "food_le_meal.joblib"))
                self.le_caf = joblib.load(os.path.join(settings.MODELS_DIR, "food_le_caf.joblib"))
            else:
                self.train()

    def predict(self, date_str: str, cafeteria_id: str, custom_features=None):
        self._load_model()
        
        df = pd.read_csv(os.path.join(settings.GENERATED_DATA_DIR, "cafeteria_sales.csv"))
        c_df = df[df['cafeteria_id'] == cafeteria_id]
        if c_df.empty: return 500, 525
        
        last_row = c_df.iloc[-1].copy()
        
        target_date = pd.to_datetime(date_str)
        last_row['weekday'] = target_date.weekday()
        last_row['cafeteria_encoded'] = self.le_caf.transform([cafeteria_id])[0]
        last_row['meal_encoded'] = self.le_meal.transform([last_row['meal_type']])[0]
        
        if custom_features:
            for k, v in custom_features.items():
                if k in last_row:
                    last_row[k] = v
                    
        x_input = pd.DataFrame([last_row[self.features]])
        pred = int(self.model.predict(x_input)[0])
        pred = max(0, pred)
        return pred, int(pred * 1.05)
