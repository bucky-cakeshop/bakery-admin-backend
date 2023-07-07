from dataclasses import dataclass
from typing import List
import datetime

from bakeryAdmin.domain.models.production.IngredientConsumeByRecipeDetail import IngredientConsumeByRecipeDetail

@dataclass
class IngredientConsumeByProductionOrderDetail:
    productionOrderDetail_id: int
    ingredientsConsumesByRecipeDetail: List[IngredientConsumeByRecipeDetail]
    expirationDate: datetime.datetime
    costPrice: float