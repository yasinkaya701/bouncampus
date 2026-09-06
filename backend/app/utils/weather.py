import pandas as pd
from datetime import date
from typing import Dict, Any, List
from app.config import settings
import os

class WeatherData:
    def __init__(self, date: date, temperature: float, humidity: float, rain: float, wind_speed: float, condition: str):
        self.date = date
        self.temperature = temperature
        self.humidity = humidity
        self.rain = rain
        self.wind_speed = wind_speed
        self.condition = condition

def get_weather(target_date: date) -> WeatherData:
    path = os.path.join(settings.GENERATED_DATA_DIR, "weather_history.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        df['date'] = pd.to_datetime(df['date']).dt.date
        row = df[df['date'] == target_date]
        if not row.empty:
            r = row.iloc[0]
            return WeatherData(target_date, r['temperature'], r['humidity'], r['rain'], r['wind_speed'], r['condition'])
    
    # Fallback
    return WeatherData(target_date, 20.0, 50.0, 0.0, 10.0, "Sunny")

def get_forecast(start_date: date, days: int = 7) -> List[WeatherData]:
    path = os.path.join(settings.GENERATED_DATA_DIR, "weather_history.csv")
    res = []
    if os.path.exists(path):
        df = pd.read_csv(path)
        df['date'] = pd.to_datetime(df['date']).dt.date
        mask = (df['date'] >= start_date)
        rows = df[mask].head(days)
        for _, r in rows.iterrows():
            res.append(WeatherData(r['date'], r['temperature'], r['humidity'], r['rain'], r['wind_speed'], r['condition']))
    
    if not res:
        for i in range(days):
            res.append(WeatherData(start_date, 20.0, 50.0, 0.0, 10.0, "Sunny"))
    return res
