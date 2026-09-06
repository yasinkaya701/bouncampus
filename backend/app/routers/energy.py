from fastapi import APIRouter
from app.schemas import EnergyForecast, EnergySaving, HourlyEnergyForecast, FloorEnergyDetail
from datetime import date, timedelta, datetime
from typing import List, Optional
from app.models.energy import EnergyModel
from app.utils.real_data_service import RealDataService

router = APIRouter(prefix="/api/v1")
e_model = EnergyModel()
real_service = RealDataService()

@router.get("/energy/{building_id}", response_model=EnergyForecast)
def get_building_energy(building_id: str, date_val: Optional[str] = None):
    d = date_val or (date.today() + timedelta(days=1)).isoformat()
    dt = datetime.fromisoformat(d)
    weekday = dt.weekday()
    
    # 1. Real weather for Boğaziçi
    live_w = real_service.fetch_live_weather()
    temp = live_w["temperature"]
    
    b = e_model.buildings.get(building_id)
    if not b:
        return EnergyForecast(
            date=d, building_id=building_id, baseline_kwh=0, optimized_kwh=0,
            savings=EnergySaving(kwh_saved=0, cost_saved_tl=0, co2_avoided_kg=0),
            hourly_forecast=[]
        )
        
    floors = b['floors']
    total_cap = max(1, b['total_capacity'])
    base_load = b['energy_profile']['base_load_kw']
    hvac_coeff = b['energy_profile']['hvac_coefficient']
    light_max = b['energy_profile']['lighting_max_kw']
    t_target = b['energy_profile']['t_target']
    
    # Historic building coefficient (Anderson, Washburn, Perkins)
    is_historic = any(h in b['name'] for h in ['Anderson', 'Washburn', 'Perkins', 'Albert Long', 'Hamlin'])
    historic_factor = 1.35 if is_historic else 1.0

    # Real hourly occupancy from 3,238 OBIKAS courses + dining dynamics
    campus_occ = real_service.get_hourly_campus_occupancy(weekday)
    b_occ = campus_occ.get(building_id, {})

    hourly_forecast = []
    total_opt = 0.0
    total_base = 0.0

    for h in range(24):
        occ_count = b_occ.get(h, 0)
        occ_ratio = min(1.0, round(occ_count / total_cap, 3))
        
        # Real baseline: standard un-optimized HVAC running all floors
        hvac_unopt = hvac_coeff * historic_factor * abs(temp - t_target)
        light_unopt = light_max * (0.8 if 8 <= h <= 20 else 0.2)
        base_h = (base_load + hvac_unopt + light_unopt)
        total_base += base_h
        
        # Real optimized: consolidate floors when classes end or occupancy is low
        floor_details = []
        h_opt = 0.0
        
        for f in range(1, floors + 1):
            # If after 18:00 and occupancy < 25%, upper floors are set to eco-mode (0.1 load)
            is_eco = (h >= 18 or h < 8) and (f > 2) and (occ_ratio < 0.25)
            
            f_base = (base_load / floors)
            if is_eco:
                f_hvac = (hvac_coeff * historic_factor * abs(temp - t_target) * 0.15) / floors
                f_light = (light_max * 0.05) / floors
                is_active = False
            else:
                f_occ = occ_ratio
                f_hvac = (hvac_coeff * historic_factor * abs(temp - t_target) * (0.3 + 0.7 * f_occ)) / floors
                f_light = (light_max * (0.1 + 0.9 * f_occ)) / floors
                is_active = True
                
            f_kwh = round(f_base + f_hvac + f_light, 2)
            h_opt += f_kwh
            floor_details.append(FloorEnergyDetail(
                floor=f, energy_kwh=f_kwh, hvac_kwh=round(f_hvac, 2),
                lighting_kwh=round(f_light, 2), is_active=is_active
            ))
            
        total_opt += h_opt
        hourly_forecast.append(HourlyEnergyForecast(
            hour=h, total_kwh=round(h_opt, 2), floor_details=floor_details
        ))

    total_base = round(total_base, 1)
    total_opt = round(total_opt, 1)
    kwh_saved = max(0.0, round(total_base - total_opt, 1))
    
    return EnergyForecast(
        date=d, building_id=building_id,
        baseline_kwh=total_base, optimized_kwh=total_opt,
        savings=EnergySaving(
            kwh_saved=kwh_saved,
            cost_saved_tl=round(kwh_saved * 2.8, 1),
            co2_avoided_kg=round(kwh_saved * 0.47, 1)
        ),
        hourly_forecast=hourly_forecast
    )

@router.get("/energy", response_model=List[EnergyForecast])
def get_all_energy(date_val: Optional[str] = None):
    d = date_val or (date.today() + timedelta(days=1)).isoformat()
    res = []
    for b_id in e_model.buildings.keys():
        res.append(get_building_energy(b_id, d))
    return res
