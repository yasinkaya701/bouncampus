from app.config import settings

def calculate_energy_savings(baseline_kwh: float, optimized_kwh: float) -> float:
    return max(0, baseline_kwh - optimized_kwh)

def calculate_co2_savings(kwh_saved: float) -> float:
    return kwh_saved * settings.CO2_PER_KWH

def calculate_food_savings(baseline_portions: int, recommended_portions: int) -> float:
    saved_portions = max(0, baseline_portions - recommended_portions)
    return saved_portions * settings.FOOD_WASTE_KG_PER_PORTION

def calculate_cost_savings(kwh_saved: float, food_kg_saved: float = 0.0) -> float:
    return kwh_saved * settings.COST_PER_KWH
