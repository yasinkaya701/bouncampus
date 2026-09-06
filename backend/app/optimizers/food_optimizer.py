class FoodOptimizer:
    def optimize(self, date, cafeteria_id, predicted_demand, menu):
        buffer_percent = 0.05
        recommended = int(predicted_demand * (1 + buffer_percent))
        baseline = int(predicted_demand * 1.15) # Assume 15% historical buffer
        waste_reduction = max(0, baseline - recommended)
        return {
            "recommended": recommended, 
            "waste_reduction": waste_reduction
        }
