import os
from app.models.occupancy import OccupancyPredictor
from app.models.food_demand import FoodDemandPredictor
from app.models.collaborative import FoodRecommender

def main():
    print("Generating data...")
    os.system("PYTHONPATH=. python app/data/generator.py")
    print("Data generated. Training models...")
    
    occ = OccupancyPredictor()
    occ.train()
    print("Occupancy model trained.")
    
    food = FoodDemandPredictor()
    food.train()
    print("Food demand model trained.")
    
    rec = FoodRecommender()
    rec.train()
    print("Collaborative model trained.")
    
    print("Done!")

if __name__ == "__main__":
    main()
