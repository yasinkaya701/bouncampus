from app.schemas import ActionItem
import uuid

class ActionEngine:
    def generate_actions(self, date, energy_recs, food_recs):
        return [
            ActionItem(id=str(uuid.uuid4()), priority="HIGH", type="energy", title="Close KB 4th Floor", description="Consolidate students to 3rd floor", impact_metric="kWh", impact_value=120, building_id="B-NORTH-KB")
        ]
