import json
import os
import pandas as pd
from app.config import settings

class EnergyModel:
    def __init__(self):
        with open(os.path.join(settings.DATA_DIR, 'campus_config.json'), 'r') as f:
            self.buildings = {b['id']: b for b in json.load(f)['buildings']}
            
    def calculate(self, building_id: str, floor: int, hour: int, temperature: float, occupancy_ratio: float):
        b = self.buildings.get(building_id)
        if not b: return 0.0, 0.0, 0.0
        
        prof = b['energy_profile']
        
        historic = b['name'] in ['Anderson Hall', 'Washburn Hall', 'Perkins Hall', 'Albert Long Hall']
        hvac_modifier = 1.2 if historic else 1.0
        
        base = prof['base_load_kw'] / b['floors']
        hvac = prof['hvac_coefficient'] * hvac_modifier * abs(temperature - prof['t_target']) * (0.3 + 0.7 * occupancy_ratio) / b['floors']
        light = prof['lighting_max_kw'] * (0.1 + 0.9 * occupancy_ratio) / b['floors']
        
        if occupancy_ratio < 0.01 and b['type'] != 'Dorm':
            hvac *= 0.1
            light *= 0.05
            
        return base + hvac + light, hvac, light
        
    def calculate_building(self, building_id, date, occupancy_forecast, weather):
        total_kwh = 0
        b = self.buildings.get(building_id)
        
        if not b or not occupancy_forecast.by_floor: return 0.0
        
        for hour in range(24):
            temp = weather.temperature
            for floor_data in occupancy_forecast.by_floor:
                floor = floor_data.floor
                occ_ratio = floor_data.hourly_occupancy[hour].occupancy_ratio
                e, _, _ = self.calculate(building_id, floor, hour, temp, occ_ratio)
                total_kwh += e
                
        return total_kwh
        
    def calculate_baseline(self, building_id, date, weather):
        return 500.0 # simplified baseline
