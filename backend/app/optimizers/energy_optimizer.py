from ortools.linear_solver import pywraplp
import json
import os
from app.config import settings

class EnergyOptimizer:
    def __init__(self):
        with open(os.path.join(settings.DATA_DIR, 'campus_config.json'), 'r') as f:
            self.buildings = {b['id']: b for b in json.load(f)['buildings']}
            
    def optimize(self, date, occupancy_forecast, weather):
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver: return []
        
        b = self.buildings.get(occupancy_forecast.building_id)
        if not b or not occupancy_forecast.by_floor: return []
        
        x = {}
        for f in range(1, b['floors'] + 1):
            x[f] = solver.IntVar(0, 1, f'x_{f}')
            
        total_cap = sum(b['floor_capacities'])
        
        # We find max occupancy across the day
        max_occ = 0
        for floor_data in occupancy_forecast.by_floor:
            for hourly in floor_data.hourly_occupancy:
                max_occ += hourly.occupancy_count
        
        max_occ = max_occ / 24 # crude average for day
        
        # Constraint: total open capacity >= expected occupancy * 1.2 buffer
        solver.Add(sum(x[f] * b['floor_capacities'][f-1] for f in range(1, b['floors'] + 1)) >= max_occ * 1.2)
        
        # Objective: minimize open floors (energy proxy)
        solver.Minimize(sum(x[f] for f in range(1, b['floors'] + 1)))
        
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            recs = []
            for f in range(1, b['floors'] + 1):
                if x[f].solution_value() < 0.5:
                    recs.append(f"Close floor {f} to save energy.")
            return recs
        return []
