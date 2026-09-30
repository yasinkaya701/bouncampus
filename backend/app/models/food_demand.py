import os

import joblib
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

from app.config import settings


class FoodDemandPredictor:
    MODEL_ID = "food-demand-xgboost"
    TRAINING_DATA_PROVENANCE = "REPOSITORY_GENERATED_DATA_UNVERIFIED"

    def __init__(self):
        self.model = None
        self.le_meal = LabelEncoder()
        self.le_caf = LabelEncoder()
        self.model_path = os.path.join(settings.MODELS_DIR, "food_xgb.joblib")
        self.features = [
            "campus_occupancy",
            "weekday",
            "meal_encoded",
            "cafeteria_encoded",
            "exam_week",
            "temperature",
            "rain",
            "event_count",
            "semester_week",
            "menu_popularity_avg",
        ]

    @property
    def training_data_path(self):
        return os.path.join(settings.GENERATED_DATA_DIR, "cafeteria_sales.csv")

    def metadata(self):
        return {
            "model_id": self.MODEL_ID,
            "forecast_provenance": "MODEL_ESTIMATE",
            "training_data_path": self.training_data_path,
            "training_data_provenance": self.TRAINING_DATA_PROVENANCE,
            "calibration_status": "NOT_CALIBRATED",
            "impact_validation_status": "NOT_PILOT_VALIDATED",
        }

    def train(self, data_path: str = None):
        data_path = data_path or self.training_data_path
        df = pd.read_csv(data_path)
        df["meal_encoded"] = self.le_meal.fit_transform(df["meal_type"])
        df["cafeteria_encoded"] = self.le_caf.fit_transform(df["cafeteria_id"])

        X = df[self.features]
        y = df["portions_sold"]

        self.model = xgb.XGBRegressor(n_estimators=100, max_depth=4, random_state=42)
        self.model.fit(X, y)
        os.makedirs(settings.MODELS_DIR, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.le_meal, os.path.join(settings.MODELS_DIR, "food_le_meal.joblib"))
        joblib.dump(self.le_caf, os.path.join(settings.MODELS_DIR, "food_le_caf.joblib"))

    def _load_model(self):
        if self.model is not None:
            return
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.le_meal = joblib.load(os.path.join(settings.MODELS_DIR, "food_le_meal.joblib"))
            self.le_caf = joblib.load(os.path.join(settings.MODELS_DIR, "food_le_caf.joblib"))
        else:
            self.train()

    def predict(
        self,
        date_str: str,
        cafeteria_id: str,
        meal_type: str | None = None,
        custom_features=None,
    ):
        """Return a point forecast; uncertainty/recommendation belongs to food_policy.

        The second tuple value is retained only for compatibility with legacy callers
        and equals the point estimate. It is not an upper bound or confidence value.
        """

        self._load_model()

        df = pd.read_csv(self.training_data_path)
        cafeteria_rows = df[df["cafeteria_id"] == cafeteria_id]
        if cafeteria_rows.empty:
            return 0, 0

        if meal_type is not None:
            meal_rows = cafeteria_rows[cafeteria_rows["meal_type"] == meal_type]
            if not meal_rows.empty:
                cafeteria_rows = meal_rows

        last_row = cafeteria_rows.iloc[-1].copy()
        selected_meal = meal_type or str(last_row["meal_type"])
        if selected_meal not in set(self.le_meal.classes_):
            selected_meal = str(last_row["meal_type"])

        target_date = pd.to_datetime(date_str)
        last_row["weekday"] = target_date.weekday()
        last_row["cafeteria_encoded"] = self.le_caf.transform([cafeteria_id])[0]
        last_row["meal_encoded"] = self.le_meal.transform([selected_meal])[0]

        if custom_features:
            for key, value in custom_features.items():
                if key in self.features:
                    last_row[key] = value

        x_input = pd.DataFrame([last_row[self.features]])
        prediction = int(self.model.predict(x_input)[0])
        prediction = max(0, prediction)
        return prediction, prediction
