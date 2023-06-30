import datetime
from dataclasses import dataclass

@dataclass
class IngredientConsumeByRecipeDetail:
    recipeDetail_id: int
    productionOrderConsume_id: int
    totalQuantity: float
    expirationDate: datetime.datetime
    unitCostPrice: float
    measureUnit_id: int
    ingredient_id: int
    
