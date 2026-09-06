import xgboost as xgb
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import LabelEncoder
from app.config import settings

class OccupancyPredictor:
    def __init__(self):
        self.model = None
        self.le = LabelEncoder()
        self.model_path = os.path.join(settings.MODELS_DIR, "occupancy_xgb.joblib")
        self.le_path = os.path.join(settings.MODELS_DIR, "occupancy_le.joblib")
        self.features = ['hour', 'weekday', 'building_encoded', 'floor', 'scheduled_students', 'total_capacity', 'exam_week', 'event_count', 'temperature', 'rain', 'semester_week', 'prev_day_occupancy', 'prev_week_same_hour']

    def train(self, data_path: str = None):
        if not data_path:
            data_path = os.path.join(settings.GENERATED_DATA_DIR, "occupancy_history.csv")
        df = pd.read_csv(data_path)
        
        df['building_encoded'] = self.le.fit_transform(df['building_id'])
        
        X = df[self.features]
        y = df['occupancy_count']
        
        self.model = xgb.XGBRegressor(n_estimators=100, max_depth=5, random_state=42)
        self.model.fit(X, y)
        
        os.makedirs(settings.MODELS_DIR, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.le, self.le_path)

    def _load_model(self):
        if not self.model:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.le = joblib.load(self.le_path)
            else:
                self.train()

    def feature_importance(self):
        self._load_model()
        importance = self.model.feature_importances_
        return dict(zip(self.features, importance))

    def predict_floor(self, date_str: str, building_id: str, floor: int, custom_features=None):
        self._load_model()
        df = pd.read_csv(os.path.join(settings.GENERATED_DATA_DIR, "occupancy_history.csv"))
        b_df = df[(df['building_id'] == building_id) & (df['floor'] == floor)].copy()
        
        if b_df.empty:
            return []
            
        b_df['building_encoded'] = self.le.transform(b_df['building_id'])
        b_df['date'] = pd.to_datetime(b_df['date'])
        
        # Simulating realistic future features based on past
        res = []
        target_date = pd.to_datetime(date_str)
        weekday = target_date.weekday()
        
        for h in range(24):
            hist_hour = b_df[b_df['hour'] == h].iloc[-1]
            row = hist_hour.copy()
            row['weekday'] = weekday
            
            if custom_features:
                for k, v in custom_features.items():
                    if k in row:
                        row[k] = v
            
            x_input = pd.DataFrame([row[self.features]])
            pred = self.model.predict(x_input)[0]
            pred = max(0, min(pred, row['total_capacity']))
            
            res.append({
                "hour": h,
                "occupancy_count": int(pred),
                "occupancy_ratio": round(pred / max(1, row['total_capacity']), 3)
            })
        return res

    def predict(self, date_str: str, building_id: str = None):
        return self.predict_floor(date_str, building_id, 1)
