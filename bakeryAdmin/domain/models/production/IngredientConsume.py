from dataclasses import dataclass

@dataclass
class IngredientConsume:
    recipeDetail_id: int
    productionOrderConsume_id: int
    
