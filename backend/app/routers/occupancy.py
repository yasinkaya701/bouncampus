from fastapi import APIRouter
from app.schemas import OccupancyForecast, OccupancyByHour, OccupancyByFloor
from datetime import date, timedelta, datetime
from typing import List, Optional
import json, os
from app.config import settings
from app.models.occupancy import OccupancyPredictor
from app.utils.real_data_service import RealDataService

router = APIRouter(prefix="/api/v1")
predictor = OccupancyPredictor()
real_service = RealDataService()

def get_buildings():
    with open(os.path.join(settings.DATA_DIR, 'campus_config.json'), 'r') as f:
        return json.load(f)['buildings']

@router.get("/occupancy", response_model=List[OccupancyForecast])
def get_all_occupancy(date_val: Optional[str] = None):
    d = date_val or (date.today() + timedelta(days=1)).isoformat()
    dt = datetime.fromisoformat(d)
    weekday = dt.weekday()
    
    # Real BOUN Schedule + Cafeteria / Canteen / Library Rush Hours
    real_occ = real_service.get_hourly_campus_occupancy(weekday)
    buildings = get_buildings()
    res = []
    
    for b in buildings:
        b_id = b['id']
        f_data = predictor.predict_floor(d, b_id, 1)
        schedule_by_hour = real_occ.get(b_id, {})
        
        # Merge real schedule & dining dynamics with ML prediction
        merged_hourly = []
        for h_item in f_data:
            h = h_item['hour']
            sched_count = schedule_by_hour.get(h, 0)
            final_count = max(h_item['occupancy_count'], sched_count)
            ratio = min(1.0, round(final_count / max(1, b['total_capacity']), 3))
            merged_hourly.append(OccupancyByHour(
                hour=h,
                occupancy_count=final_count,
                occupancy_ratio=ratio
            ))
            
        res.append(OccupancyForecast(date=d, building_id=b_id, total_hourly=merged_hourly))
    return res

@router.get("/occupancy/{building_id}", response_model=OccupancyForecast)
def get_building_occupancy(building_id: str, date_val: Optional[str] = None):
    d = date_val or (date.today() + timedelta(days=1)).isoformat()
    dt = datetime.fromisoformat(d)
    weekday = dt.weekday()
    
    b = next((x for x in get_buildings() if x['id'] == building_id), None)
    if not b:
        return OccupancyForecast(date=d, building_id=building_id, total_hourly=[])
    
    real_occ = real_service.get_hourly_campus_occupancy(weekday).get(building_id, {})
    by_floor = []
    total_hourly = [{"hour": h, "occupancy_count": 0, "occupancy_ratio": 0.0} for h in range(24)]
    
    for f in range(1, b['floors'] + 1):
        f_data = predictor.predict_floor(d, building_id, f)
        hourly_occ = []
        floor_cap = b['floor_capacities'][f-1] if 'floor_capacities' in b and f-1 < len(b['floor_capacities']) else (b['total_capacity'] // b['floors'])
        
        for item in f_data:
            h = item['hour']
            # Distribute scheduled students across active floors
            sched_floor = real_occ.get(h, 0) // b['floors']
            c = max(item['occupancy_count'], sched_floor)
            r = min(1.0, round(c / max(1, floor_cap), 3))
            hourly_occ.append(OccupancyByHour(hour=h, occupancy_count=c, occupancy_ratio=r))
            total_hourly[h]['occupancy_count'] += c
            
        by_floor.append(OccupancyByFloor(floor=f, hourly_occupancy=hourly_occ))
        
    for i in range(24):
        total_hourly[i]['occupancy_ratio'] = min(1.0, round(total_hourly[i]['occupancy_count'] / max(1, b['total_capacity']), 3))
        
    return OccupancyForecast(
        date=d,
        building_id=building_id,
        total_hourly=[OccupancyByHour(**x) for x in total_hourly],
        by_floor=by_floor
    )
