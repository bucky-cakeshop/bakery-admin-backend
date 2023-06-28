from dataclasses import dataclass
from typing import List

from bakeryAdmin.domain.models.production.IngredientConsumeByRecipeDetail import IngredientConsumeByRecipeDetail

@dataclass
class IngredientConsumeByProductionOrderDetail:
    productionOrderDetail_id: int
    ingredientsConsumesByRecipeDetail: List[IngredientConsumeByRecipeDetail]