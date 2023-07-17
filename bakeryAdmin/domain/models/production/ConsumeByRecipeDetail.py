import datetime
from dataclasses import dataclass

@dataclass
class ConsumeByRecipeDetail:
    recipeDetail_id: int
    totalQuantity: float
    expirationDate: datetime.datetime
    unitCostPrice: float

@dataclass
class IngredientConsumeByRecipeDetail:
    recipeDetail_id: int
    productionOrderConsume_id: int
    totalQuantity: float
    expirationDate: datetime.datetime
    unitCostPrice: float
    measureUnit_id: int
    ingredient_id: int
    
@dataclass
class ProductConsumeByRecipeDetail:
    recipeDetail_id: int
    productionOrderConsumeProduct_id: int
    totalQuantity: float
    expirationDate: datetime.datetime
    unitCostPrice: float
    measureUnit_id: int
    product_id: int
