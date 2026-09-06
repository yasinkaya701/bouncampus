from fastapi import APIRouter
from app.schemas import ActionItem
from datetime import date, timedelta
from typing import List, Optional
import uuid
from app.utils.real_data_service import RealDataService

router = APIRouter(prefix="/api/v1")
real_service = RealDataService()

@router.get("/actions", response_model=List[ActionItem])
def get_actions(date_val: Optional[str] = None):
    d = date_val or (date.today() + timedelta(days=1)).isoformat()
    menu = real_service.fetch_live_cafeteria_menu()
    weather = real_service.fetch_live_weather()
    temp = weather["temperature"]
    
    return [
        ActionItem(
            id=str(uuid.uuid4()),
            priority="HIGH",
            type="food",
            title=f"Peak Lunch Surge in Kuzey Yemekhanesi: {menu['main_dish']}",
            time="11:45 - 13:45",
            location="Kuzey Yemekhanesi & Piramit",
            description=f"Classroom dismissal surge at 12:00. 635 students expected simultaneous. Today's official dish: {menu['main_dish']} ({menu['calories']} kcal). Pre-portion 1,420 servings to prevent queuing and food waste.",
            impact_value=48.0,
            impact_unit="kg"
        ),
        ActionItem(
            id=str(uuid.uuid4()),
            priority="HIGH",
            type="energy",
            title="Consolidate Kare Blok (KB) Evening Study Groups",
            time="18:00 - 22:00",
            location="Kare Blok",
            description=f"Registration schedule has 0 lectures after 18:00. Consolidate remaining students into Floors 1-2. Power down Floors 3-5 HVAC (Outdoor: {temp}°C).",
            impact_value=175.0,
            impact_unit="kWh"
        ),
        ActionItem(
            id=str(uuid.uuid4()),
            priority="MEDIUM",
            type="space",
            title="Redirect South Campus Lunch Overflow to Orta Kantin",
            time="12:15 - 13:15",
            location="Güney Yemekhanesi & Dodge Hall",
            description="Güney Yemekhanesi (159 seats) projected at 96% capacity (152 students). Open auxiliary seating in Orta Kantin (Dodge Hall).",
            impact_value=75.0,
            impact_unit="students"
        ),
        ActionItem(
            id=str(uuid.uuid4()),
            priority="MEDIUM",
            type="energy",
            title="New Hall (NH) Midday Lecture Hall Eco-Ventilation",
            time="12:00 - 13:00",
            location="Yeni Bina (NH)",
            description="Tiered auditoriums NH 101, 201, 301, 401 empty during lunch break. Shift ventilation to eco-mode.",
            impact_value=90.0,
            impact_unit="kWh"
        ),
        ActionItem(
            id=str(uuid.uuid4()),
            priority="LOW",
            type="energy",
            title="Aptullah Kuran Library Night HVAC Optimization",
            time="21:00 - 02:00",
            location="Aptullah Kuran Kütüphanesi",
            description="Consolidate late-night study students into Ground & 1st floor reading halls.",
            impact_value=45.0,
            impact_unit="kWh"
        )
    ]
